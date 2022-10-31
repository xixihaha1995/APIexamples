from os import makedirs, path
from shutil import rmtree
import sys
from threading import Thread
from time import sleep

ProductsDir = 'C:/EnergyPlusV22-1-0'
RepoRoot = 'C:/EnergyPlusV22-1-0'
IDFDir = 'ExampleFiles'

sys.path.insert(0, str(ProductsDir))
from pyenergyplus.api import EnergyPlusAPI


def thread_function(_working_dir: str):
    print(f"Thread: Running at working dir: {_working_dir}")
    if path.exists(_working_dir):
        rmtree(_working_dir)
    makedirs(_working_dir)
    api = EnergyPlusAPI()
    state = api.state_manager.new_state()
    e_args='-d',_working_dir,'-a', '-w','USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw', '5ZoneAirCooled.idf'
    api.runtime.run_energyplus(state, e_args)


threads = list()
for index in range(3):
    working_dir = f"temp/test_thread_{index}"
    print(f"Main    : create and start thread at working directory: {working_dir}.")
    x = Thread(target=thread_function, args=(working_dir,))
    threads.append(x)
    x.start()
    sleep(0)