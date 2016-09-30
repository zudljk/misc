import os
import sys

##Virtualenv Settings
activate_this = '/home/ubuntu/workspace/blogrest/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

##Replace the standard out
sys.stdout = sys.stderr

##Add this file path to sys.path in order to import settings
sys.path.insert(0, '/home/ubuntu/workspace/blogrest')

##Add this file path to sys.path in order to import app
sys.path.append('/home/ubuntu/workspace/blogrest')

##Create appilcation for our app
from blogrest import app as application
