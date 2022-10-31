import argparse
import os
import sys
import shutil
import threading
from threading import Thread
folder_with_pyenergyplus = 'C:/EnergyPlusV22-1-0'
sys.path.insert(0, folder_with_pyenergyplus)
from pyenergyplus.api import EnergyPlusAPI

def thread_function(api_instance, tmp_run_dir, weather_file, idf_to_run):
    print("Thread %s: starting" % threading.get_ident())
    state = api_instance.state_manager.new_state()
    api_instance.runtime.run_energyplus(state, ['-d', tmp_run_dir, '-w', weather_file, idf_to_run])
    print("Thread %s: finishing" % threading.get_ident())

path_to_idf = '5ZoneAirCooled.idf'
weather_file_to_use = 'USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw'
a = EnergyPlusAPI()
'''No threads. ✅
state = a.state_manager.new_state()
# temp_run_dir = os.path.join(os.getcwd(), 'temp_run_dir')
ret1 = a.runtime.run_energyplus(state, ['-d', temp_run_dir, '-w', weather_file_to_use, path_to_idf])
a.state_manager.reset_state(state)
ret2 = a.runtime.run_energyplus(state, ['-d', temp_run_dir, '-w', weather_file_to_use, path_to_idf])
sys.exit(ret1 + ret2)
'''


'''With threads. ❌'''
for run_in_dir in ['run1', 'run2']:
    # clean out an existing run directory and remake it, moving into that directory as needed
    #project absolute path
    project_path = os.path.dirname(os.path.abspath(__file__))
    temp_run_dir = os.path.join(project_path, run_in_dir)
    if os.path.exists(run_in_dir):
        shutil.rmtree(run_in_dir)
    os.makedirs(run_in_dir)
    t = Thread(target=thread_function, args=(a,temp_run_dir, weather_file_to_use, path_to_idf))
    t.start()
    t.join()