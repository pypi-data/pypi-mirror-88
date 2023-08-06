
import subprocess, os, sys, shutil, signal, logging
import vytools.utils
import vytools.compose
from termcolor import cprint
from vytools.config import ITEMS, CONFIG

global SHUTDOWN
SHUTDOWN = {'path':'','down':[],'logs':[],'services':[]}
def stop():
  logs = subprocess.run(SHUTDOWN['logs'], cwd=SHUTDOWN['path'], stdout=subprocess.PIPE)
  subprocess.run(SHUTDOWN['down'], cwd=SHUTDOWN['path'])
  return logs

def compose_exit_code(eppath):
  success = True
  try:
    anyzeros = False
    if not os.path.isdir(eppath):
      return False

    # Get services, wish there was a better way...
    services = []
    for s in subprocess.check_output(SHUTDOWN['services'], 
        cwd=SHUTDOWN['path']).decode('ascii').strip().split('\n'):
      count = 1
      while True:
        name = SHUTDOWN['jobid']+'_'+s+'_'+str(count)
        count+=1
        if name not in services:
          break
      services.append(name)

    for service in services:
      try:
        exitcode = subprocess.check_output(['docker', 'container', 'inspect',service,'--format','{{.State.ExitCode}}']).decode('ascii').strip()
      except Exception as exc:
        success = False
        exitcode = '1'
        logging.error('Failed to get exit code for {s}: {e}'.format(s=service, e=exc))
      anyzeros |= int(exitcode) == 0
      logging.info('---- Service '+service+' exited with code '+exitcode)
    return success and anyzeros
  except Exception as exc:
    logging.error('Failed to get exit codes'+str(exc))
    return False

ORIGINAL_SIGINT = signal.getsignal(signal.SIGINT)
def exit_gracefully(signum, frame):
  signal.signal(signal.SIGINT, ORIGINAL_SIGINT) # restore the original signal handler
  logs = stop()
  sys.exit(signum) # TODO is this right? pass out signum?

def runpath(epid, jobpath=None):
  if jobpath is None: jobpath = CONFIG.job_path()
  return os.path.join(jobpath,epid) if epid and jobpath else None

def build(rootcompose, build_arg_dict, items, built, build_level, data=None, data_mods=None, eppath=None):
  if data is None:
    data = {}
  elif type(data) == str and data in items:
    data = items[data]['data']
  return vytools.compose.build({'name':rootcompose,'parent_data':data,'data_mods':data_mods},
                        build_arg_dict, items, built, build_level,eppath=eppath)

def run(epid, compose_name, build_arg_dict={}, items=None, clean=False, data=None, data_mods=None, jobpath=None):
  global SHUTDOWN

  if items is None: items = ITEMS
  # TODO test epid, lower case, alphanumeric starts with alpha?
  deplist = [compose_name,data] if type(data) == str else [compose_name]
  results = {'is_data_modified':data is not None or data_mods is not None}
  eppath = runpath(epid,jobpath)
  if not eppath: return False

  if clean:
    try:
      shutil.rmtree(eppath)
    except Exception as exc:
      logging.error('Failed to clean folder {n}'.format(n=eppath))
      return False

  os.makedirs(eppath,exist_ok=True)
  build_args = build_arg_dict.copy()
  built = {}
  # Compile compose files and any volumes
  cmds = build(compose_name, build_args, items, built, -1, data, data_mods, eppath=eppath) # get components
  if cmds == False: return False
  cmd = ['docker-compose'] + cmds + ['--project-name', epid]

  cmdup = cmd+['up', '--abort-on-container-exit']
  SHUTDOWN['down'] = cmd + ['down','--volumes']
  SHUTDOWN['jobid'] = epid
  SHUTDOWN['path'] = eppath
  SHUTDOWN['logs'] = cmd + ['logs']
  SHUTDOWN['services'] = cmd + ['ps','--services']
  try:
    signal.signal(signal.SIGINT, exit_gracefully)
  except Exception as exc:
    logging.warning(str(exc))
    
  with open(os.path.join(eppath,'start.sh'),'w') as w2:
    w2.write(' '.join(cmdup))

  cprint('Episode Path = '+eppath,color='cyan')
  proc = subprocess.run(cmdup, cwd=eppath)
  compose_exit = compose_exit_code(eppath)
  stop()
  
  results['passed'] = compose_exit and proc.returncode == 0
  logging.info(' --- done with episode execution: '+epid)
  logging.info(' --- done reading output of run episode: '+epid)
  
  checked = vytools.utils.get_repo_versions(deplist, items)
  for v in checked.values():
    cprint(v,'yellow' if v.endswith('+') else 'green')
  results['repos'] = [v for v in checked.values()]

  # if episode['repo'] in checked:
  #   del checked[episode['repo']] # Remove the repository containing this episode

  return results
