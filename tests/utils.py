import os 
import sys

def add_root_to_path():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    sys.path.append(root_dir)
    return root_dir