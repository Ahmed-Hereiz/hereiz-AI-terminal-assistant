import argparse
import os 
import sys

def add_root_to_path():
    hereiz_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
    sys.path.append(hereiz_root)
    return hereiz_root

def get_arguments():
    parser = argparse.ArgumentParser(description="Terminal Chatbot", allow_abbrev=False)
    parser.add_argument("--ask", "-a", type=str, help="Your question to the model")
    args, unknown = parser.parse_known_args()

    if unknown:
        print(f"Ignoring unknown argument(s): {', '.join(unknown)}")

    return args