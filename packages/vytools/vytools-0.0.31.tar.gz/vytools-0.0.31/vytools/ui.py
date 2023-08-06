import http.server, os, socketserver, json, copy, sys

from multiprocessing import Queue, Process
from multiprocessing.connection import Listener
import threading, time
from pathlib import PurePath, Path
from urllib.parse import urlparse
from vytools.config import CONFIG, ITEMS
import vytools.utils as utils
import vytools.object
import vytools.episode
import vytools.composerun
from io import BytesIO

import vytools.utils as utils
import logging
BASEPATH = os.path.dirname(os.path.realpath(__file__))

def parse(name, pth, reponame, items):
  item = {
    'name':name,
    'repo':reponame,
    'thingtype':'ui',
    'depends_on':[],
    'path':pth
  }
  return utils._add_item(item, items, True)

def find_all(items, contextpaths=None):
  success = utils.search_all(None, parse, items, is_ui=True, contextpaths=contextpaths)
  return success

def set_headers(self,typ,x):
  self.send_response(200)
  self.send_header("Content-type", typ)
  self.end_headers()
  self.wfile.write(x)

def _send(self, pth):
  typ = None
  binary = False
  if pth:
    ext = pth.rsplit('.',1)[-1]
    if len(ext) < len(pth): ext = '.'+ext
    if ext in self.extensions_map:
      typ = self.extensions_map[ext]
      binary = ext in self.binary_types
  if not typ:
    logging.error('Failed to send to client: '+str(pth))
    set_headers(self,'application/json',json.dumps({}).encode())
  elif not binary:
    set_headers(self, typ, bytes(Path(pth).read_text(), "utf8"))
  else:
    set_headers(self, typ, Path(pth).read_bytes())

def get_ui(req, items):
  ui_name = req.get('name','')
  ui = items.get(ui_name,None)
  loaded = {'html':'Could not find '+ui_name}
  if ui:
    loaded['name'] = ui_name
    loaded['html'] = Path(ui['path']).read_text()
  return loaded

def get_episode(req, items):
  episode_name = req.get('name','')
  episode = items.get(episode_name,{})
  loaded = {}
  if episode:
    loaded = get_compose({'name':episode.get('compose','')},items)
    loaded['name'] = episode_name
    obj = items.get(episode.get('data',''),None)
    if obj:
      loaded['calibration'] = vytools.object.expand(obj['data'],obj['definition'],items)
      loaded['definition'] = obj['definition']
  return loaded

def get_compose(req,items):
  compose_name = req.get('name','')
  compose = items.get(compose_name,{})
  loaded = {}
  if compose:
    loaded['name'] = compose_name
    loaded['html'] = 'Could not find '+compose.get('ui','')
    ui = items.get(compose.get('ui',''),None)
    if ui: loaded['html'] = Path(ui['path']).read_text()
  return loaded

def get_all_queue(q):
  lst = []
  try:
    while True: lst.append(q.get(block=False))
  except Exception as exc:
    pass
  return lst

def _listener(to_browser_client, to_engine_client, listener_port=17172):
  address = ('0.0.0.0', listener_port) # todo is this ok? localhost and 127.0.0.1 can't be seen from inside a container
  with Listener(address) as listener: #, authkey=b'secret password') as listener:
    while True:
      try:
        with listener.accept() as conn:
          while True:
            snd = get_all_queue(to_engine_client)
            if len(snd) > 0:
              conn.send(snd[-1]) # Just send the last one!
            if conn.poll(timeout=0.05):
              x = conn.recv()
              to_browser_client.put(x) # Block until you get something from the client
      except Exception as exc:
        logging.error('Broken connection: '+str(exc))

def server(items=None, port=17171, ui_subscribers=None, listener_port=17172, menu=None, jobpath=None):
  if items is None: items = ITEMS
  if ui_subscribers is None: ui_subscribers = {}
  to_engine_client = Queue()
  to_browser_client = Queue()
  MESSAGES = {}
  THREAD = None
  class VyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    binary_types = ['.ico','.png','.jpg']
    extensions_map = {
        '': 'application/octet-stream',
        '.manifest': 'text/cache-manifest',
        '.html': 'text/html',
        '.png': 'image/png',
        '.ico': 'image/ico',
        '.jpg': 'image/jpg',
        '.svg':	'image/svg+xml',
        '.css':	'text/css',
        '.js':'application/x-javascript',
        '.wasm': 'application/wasm',
        '.json': 'application/json',
        '.xml': 'application/xml',
    }
    def build_run(self, req, action):
      nonlocal THREAD
      if action not in ['build','run']: return {}
      kwargs = req['kwargs'] if 'kwargs' in req else {}
      kwargs['jobpath'] = jobpath
      d = {'starting':THREAD is None or not THREAD.is_alive()}
      if d['starting']:
        if action == 'build':
          THREAD = threading.Thread(target=vytools.build, args=(req['list'],items,), kwargs=kwargs, daemon=True)
        elif action == 'run':
          THREAD = threading.Thread(target=vytools.run, args=(req['list'],items,), kwargs=kwargs, daemon=True)
        THREAD.start()
      return d

    def end_headers (self):
      self.send_header('Access-Control-Allow-Origin', '*')
      http.server.SimpleHTTPRequestHandler.end_headers(self)

    def do_GET(self):
      pth = 'ui:'+self.path
      if self.path == '/':
        _send(self,os.path.join(BASEPATH, 'vybase', 'main.html'))
      elif self.path == '/favicon.ico':
        _send(self,os.path.join(BASEPATH, 'vybase', 'favicon.ico'))
      elif self.path.startswith('/vybase/'):
        try:
          pth = os.path.join(BASEPATH, self.path.strip('/'))
          pth = Path(pth).resolve()
          if Path(os.path.join(BASEPATH,'vybase')) in pth.parents:
            _send(self, str(pth))
        except Exception as exc:
          pass
      elif self.path.startswith('/vy/') and pth in items:
        _send(self, items[pth]['path'])
      else:
        self.send_error(404, "File not found")
        logging.error('Failed to find: '+self.path)

    def do_POST(self):
      nonlocal MESSAGES
      try:
        if self.path == '/__init__':
          d = {
            'items':items,
            'server_subscribers':[k for k in ui_subscribers.keys()],
            'menu':CONFIG.get('menu') if menu is None else menu
          }
        else:
          content_length = int(self.headers['Content-Length'])
          req = json.loads(self.rfile.read(content_length).decode('utf-8'))
          d = {}
          if self.path == '/__compose__':
            d = get_compose(req, items)
          elif self.path == '/__item__':
            pth = items.get(req.get('name',None),{}).get('path',None)
            if pth:
              try:
                d = {'text':Path(pth).read_text()}
              except Exception as exc:
                logging.error('Failed to read item: {e}'.format(e=exc))
          elif self.path == '/__messages__':
            somethingrunning = THREAD is not None and THREAD.is_alive()
            if somethingrunning and 'running' not in MESSAGES:
              MESSAGES['running'] = {'level':'info','message':'Something is running'}
            elif not somethingrunning and 'running' in MESSAGES:
              del MESSAGES['running']
            d = {'messages':[v for k,v in MESSAGES.items()]}
          elif self.path == '/__build__':
            d = self.build_run(req,'build')
          elif self.path == '/__run__':
            d = self.build_run(req,'run')
          elif self.path == '/__menu__':
            if menu is None: CONFIG.set('menu',req)
          elif self.path == '/__listener__':
            if bool(req):
              to_engine_client.put(req)
            d = get_all_queue(to_browser_client)
          elif self.path == '/__ui__':
            d = get_ui(req, items)
          elif self.path == '/__episode__':
            d = get_episode(req, items)
          elif self.path == '/__artifact__':
            episode_name = req.get('name','')
            artifact_name = req.get('artifact','_')
            apaths = vytools.episode.artifact_paths(episode_name, items, jobpath=jobpath)
            if artifact_name in apaths:
              _send(self, apaths[artifact_name])
            else:
              logging.error('Could not find artifact {n} in {l}'.format(n=artifact_name,l=','.join(apaths)))
              _send(self, None)
            return
          else:
            topic = self.path.replace('/','',1)
            d = ui_subscribers[topic](req) if topic in ui_subscribers else {}
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(d).encode())
      except Exception as exc:
        logging.error(str(exc))

    def log_message(self, format, *args):
      return

  Process(target=_listener, args=(to_browser_client, to_engine_client, listener_port), daemon=True).start()
  logging.info('Serving vytools on http://localhost:{p}'.format(p=port))
  socketserver.TCPServer.allow_reuse_address = True
  if sys.version_info[0] >= 3 and sys.version_info[1] >= 6:
    with socketserver.TCPServer(("", port), VyHttpRequestHandler) as httpd:
      httpd.serve_forever()
  else:
    httpd = socketserver.TCPServer(("", port), VyHttpRequestHandler)
    httpd.serve_forever()
