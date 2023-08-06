
import vytools.utils
import vytools.compose
import vytools.definition
import vytools.object
import vytools.composerun
from termcolor import cprint
from pathlib import Path
from vytools.config import CONFIG
import re, json, shutil, os, yaml, subprocess, sys
import signal
import cerberus
import logging

SCHEMA = vytools.utils.BASE_SCHEMA.copy()
SCHEMA.update({
  'thingtype':{'type':'string', 'allowed':['episode']},
  'finished': {'type':'string', 'maxlength': 64},
  'tags':{'type':'list','schema': {'type': 'string', 'maxlength':64}},
  'compose':{'type':'string', 'maxlength': 64},
  'course':{'type':'string', 'maxlength': 64},
  'passed':{'type':'boolean'},
  'expectation':{'type':'boolean'},
  'data':{'type': 'string', 'maxlength': 64},
  'data_modified':{'type': 'boolean', 'required': False}
})
VALIDATE = cerberus.Validator(SCHEMA)

def parse(name, pth, reponame, items):
  item = {
    'name':name,
    'repo':reponame,
    'thingtype':'episode',
    'path':pth
  }
  type_name = 'episode:' + name
  item['depends_on'] = []
  try:
    with open(pth,'r') as r:
      content = json.loads(r.read())
      for sc in SCHEMA:
        if sc in content:
          item[sc] = content[sc]
      vytools.utils._check_add(item['compose'], 'compose', item, items, type_name)
      vytools.utils._check_add(item['data'], 'object', item, items, type_name)
    return vytools.utils._add_item(item, items, VALIDATE)
  except Exception as exc:
    logging.error('Failed to parse episode "{n}" at "{p}": {e}'.format(n=name, p=pth, e=exc))
    return False

def find_all(items, contextpaths=None):
  return vytools.utils.search_all(r'(.+)\.episode\.json', parse, items, contextpaths=contextpaths)

def build(type_name, build_arg_dict, items, built, build_level, data=None, data_mods=None, eppath=None):
  item = items[type_name]
  rootcompose = item['compose']
  objdata = item['data']
  if data is None:
    data = items[objdata]['data'] if objdata in items else {}
  return vytools.composerun.build(rootcompose, build_arg_dict, items, built, build_level, data, data_mods, eppath=eppath)

def get_episode_id(episode):
  return None if '..' in episode['name'] else episode['name'].lower()

def artifact_paths(episode_name, items, jobpath=None):
  if episode_name not in items: return {}
  episode = items[episode_name]
  epid = get_episode_id(episode)
  eppath = vytools.composerun.runpath(epid,jobpath=jobpath)
  return vytools.compose.artifact_paths(episode['compose'], items, eppath=eppath)

def run(type_name, build_arg_dict, items, clean, data=None, data_mods=None, jobpath=None):
  if type_name not in items: return False
  episode = items[type_name]
  epid = get_episode_id(episode)
  eppath = vytools.composerun.runpath(epid,jobpath=jobpath)
  if epid is None or eppath is None: return False
  if data is None: data = episode['data']
  compose_name = episode['compose']
  results = vytools.composerun.run(epid, compose_name, build_arg_dict, items, clean, data=data, data_mods=data_mods, jobpath=jobpath)
  if results and eppath and os.path.exists(eppath):
    results['artifacts'] = vytools.compose.artifact_paths(compose_name, items, eppath=eppath)
    with open(os.path.join(eppath, episode['name']+'.job.json'),'w') as w2:
      w2.write(json.dumps(results))
  return results

