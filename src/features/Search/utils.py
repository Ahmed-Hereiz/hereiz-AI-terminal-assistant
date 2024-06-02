import argparse
import os 
import sys

def add_root_to_path():
    hereiz_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
    sys.path.append(hereiz_root)
    return hereiz_root

def get_arguments_search():
    parser = argparse.ArgumentParser(description="Terminal Search agent", allow_abbrev=True)
    parser.add_argument("--search", "-s", type=str, help="Your query to search for with AI")
    args, unknown = parser.parse_known_args()

    if unknown:
        print(f"Ignoring unknown argument(s): {', '.join(unknown)}")

    return args

def get_arguments_searchopen():
    parser = argparse.ArgumentParser(description="Terminal Search Model", allow_abbrev=True)
    parser.add_argument("--searchopen", "-so", type=str, help="Your query to search for with AI")
    args, unknown = parser.parse_known_args()

    if unknown:
        print(f"Ignoring unknown argument(s): {', '.join(unknown)}")

    return args

def get_arguments_fullsearch():
    parser = argparse.ArgumentParser(description="Terminal Search Model", allow_abbrev=True)
    parser.add_argument("--fullsearch", "-sso", type=str, help="Your query to search for with AI")
    args, unknown = parser.parse_known_args()

    if unknown:
        print(f"Ignoring unknown argument(s): {', '.join(unknown)}")

    return args