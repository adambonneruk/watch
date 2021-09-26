"""watch a given directory for file changes using the command line, useful for demos"""
import os, sys, time, argparse, math
from colour import Colour

def full_path(path):
    """fixes /'s and used to expand an initial path component ~ to user’s home directory"""
    full_path = str(os.path.expanduser(path)).replace("/","\\")

    # consistent full path name ending with "/" for pretty print
    if not full_path[:1] == "/":
        full_path = full_path + "/"

    return full_path

def scan_filepaths(path):
    """navigate the supplied path and return all files (including hidden) as list"""
    filepaths = []

    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root,file)
            filepaths.append(filepath[len(path):])
        for dir in dirs:
            filepath = os.path.join(root,dir)
            filepaths.append(filepath[len(path):] + "\\")

    return filepaths

def pretty_print(path_and_status, verbose: bool):
    """using the colourise function in colour module, print the paths red or green"""
    colour = Colour()
    os.system("cls")
    for path, status in path_and_status.items():
        if status == "add":
            colour.print(path,Colour.GREEN)
        elif status == "del":
            colour.print(path,Colour.RED)
        elif status == "gon" and verbose:
            colour.print(path,Colour.GRAY)
        elif status == "nod":
            print(path)

def update_path_and_statuses(path_and_status, current_paths, new_paths):
    """update the PaS dictionary with a new set of old and new paths"""
    # look into the dictionary...
    for path, status in path_and_status.items():
        # ...remove really old items (anything that was removed last time)
        if status == "del":
            path_and_status.update({path:"gon"})
        # ...set everything else now to removed
        if status == "nod" or status == "add":
            path_and_status.update({path:"del"})

    # look at the new filepath array (path_delta), what is nod and add?
    for new_path in new_paths:
        if new_path in current_paths:
            path_and_status.update({new_path:"nod"}) # both lists, so no diference
        else:
            path_and_status.update({new_path:"add"}) # only new, so add

    # finally sort alphabetically
    path_and_status_a2z = dict(sorted(path_and_status.items()))
    return path_and_status_a2z

def dir_path(string):
    if os.path.isdir(full_path(string)): # also os.path.exists()
        return string
    else:
        raise NotADirectoryError("Not a Valid Directory")

def main():
    """main function, prints out the file paths, then starts a loop to check changes before printing"""

    parser = argparse.ArgumentParser()
    parser.add_argument('path',
                        nargs='?',
                        type=dir_path,
                        help='file path to watch (default: current)'
                        )
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        dest='verbose',
                        help='preserve output'
                        )
    parser.add_argument('-t', '--tick',
                        dest='tick',
                        type=int,
                        default=1.5,
                        help='clock (refresh) tick rate'
                        )
    args = parser.parse_args()

    # if theres a path passed to the function, use it, otherwise use the current working directory
    if args.path:
        req_path = full_path(args.path)
    else:
        req_path = full_path(os.getcwd())

    # calculate tick rate for refresh and rescan after difference
    tick_refresh = math.floor(args.tick)/10
    tick_rescan = args.tick

    # build the dictionary of paths and statuses
    path_and_status = {}
    """ nod = no difference
        add = added file
        del = removed file
        gon = gone forever
    """
    paths = scan_filepaths(req_path)
    for path in paths:
        path_and_status.update({path:"nod"})

    # sort and print the paths
    path_and_status_a2z = dict(sorted(path_and_status.items()))
    pretty_print(path_and_status_a2z, args.verbose)

    while True:
        # while in the loop, scan the filepaths again (new_paths) for a delta comparison
        new_paths = scan_filepaths(req_path)

        if paths == new_paths:
            time.sleep(tick_refresh)

        else:
            time.sleep(tick_rescan) # whoa theres a difference, lets pause a bit, then scan again
            new_paths = scan_filepaths(req_path)
            path_and_status = update_path_and_statuses(path_and_status, paths, new_paths)
            paths = new_paths
            pretty_print(path_and_status, args.verbose)

if __name__ == "__main__":
    #main function, wrapped in a try to catch Ctrl + C keyboard exception (while sleeping)
    try:
        main()
    except KeyboardInterrupt: # sleep throws this exception if we Ctrl + C
        sys.exit(0)