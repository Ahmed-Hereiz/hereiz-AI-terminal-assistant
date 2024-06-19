import os 
import sys

def add_root_to_path():
    hereiz_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    sys.path.append(hereiz_root)
    return hereiz_root
