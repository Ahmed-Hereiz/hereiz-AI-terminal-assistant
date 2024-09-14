import sys
from run_search import handle_search
# from run_searchopen import handle_searchopen
# from run_fullsearch import handle_fullsearch

if __name__ == "__main__":
    if '--search' in sys.argv or '-s' in sys.argv:
        handle_search()
    # elif '--searchopen' in sys.argv or '-so' in sys.argv:
    #     handle_searchopen()
    # elif '--fullsearch' in sys.argv or '-sso' in sys.argv:
    #     handle_fullsearch()
    # else:
    #     print("Usage: hereiz --search 'your search query' or hereiz --searchopen 'your search query'")