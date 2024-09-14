import argparse
import os 
import sys

def add_root_to_path():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
    sys.path.append(root_dir)
    return root_dir

def get_arguments():
    parser = argparse.ArgumentParser(description="Terminal Chatbot", allow_abbrev=False)
    parser.add_argument("--ask", "-a", type=str, required=True, help="Your question to the model")
    parser.add_argument("--human-feedback", "-H", action="store_true", help="Enable human feedback")
    args, unknown = parser.parse_known_args()

    if unknown:
        print(f"Ignoring unknown argument(s): {', '.join(unknown)}")
        return 1

    return args