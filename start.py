import sys
import os

# Setting dynamic path to import other modules
# this can be avoided by  os.env[$path] or manual os environment path setting
# Please set this path in system environment to avoid some technical challenges
# I like to control mostly in coding....

environment_path = os.getcwd() + '/' + 'control_manager/concurent_framework'
if environment_path not in sys.path:
    sys.path.append(environment_path)

# importing Control manager to start the concurentFramework
# This will initiate all the product components for services.
from control_manager import ControlManager

# String the product
ControlManager.start_services('framework_control_manager')
