import argparse
from multiprocessing import Process, freeze_support
import os
import sys
import shutil
import threading
from threading import Thread
folder_with_pyenergyplus = 'C:/EnergyPlusV22-1-0'
sys.path.insert(0, folder_with_pyenergyplus)
from pyenergyplus.api import EnergyPlusAPI

def child_function(tmp_run_dir, weather_file, idf_to_run):
    info("child process")
    api_instance = EnergyPlusAPI()
    state = api_instance.state_manager.new_state()
    api_instance.runtime.run_energyplus(state, ['-d', tmp_run_dir, '-w', weather_file, idf_to_run])
def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

if __name__ == '__main__':
    # freeze_support()
    path_to_idf = '5ZoneAirCooled.idf'
    weather_file_to_use = 'USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw'
    info('parent process')
    for run_in_dir in ['parallel_run1', 'parallel_run2']:
        # clean out an existing run directory and remake it, moving into that directory as needed
        #project absolute path
        project_path = os.path.dirname(os.path.abspath(__file__))
        temp_run_dir = os.path.join(project_path, run_in_dir)
        if os.path.exists(run_in_dir):
            shutil.rmtree(run_in_dir)
        os.makedirs(run_in_dir)
        p = Process(target=child_function,
                    args=(temp_run_dir, weather_file_to_use, path_to_idf))
        p.start()
        print("Process started: ", p)