"""watch a given directory for file changes using the command line, useful for demos"""
import os, sys, re, time
from colour import colourise

def full_path(path):
    """fixes /'s and used to expand an initial path component ~ to user’s home directory"""
    full_path = str(os.path.expanduser(path)).replace("/","\\")

    return full_path

def scan_filepaths(path):
    """navigate the supplied path and return all files (including hidden) as list"""
    filepaths = []

    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root,file)
            filepaths.append(filepath[len(path)+1:])

    return filepaths

def pretty_print(pas):
    """using the colourise function in colour module, print the paths red or green"""
    os.system("cls")
    for path, status in pas.items():
        if status == "add":
            print(colourise(path,"green"))
        elif status == "del":
            print(colourise(path,"red"))
        elif status == "gon":
            print(colourise(path,"grey"))
        else:
            print(colourise(path,"white"))

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

def main():
    """main function, prints out the file paths, then starts a loop to check changes before printing"""

    # if theres a path passed to the function, use it, otherwise use the current working directory
    if (len(sys.argv) > 1):
        req_path = full_path(sys.argv[1])
    else:
        req_path = full_path(os.getcwd())

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

    # print the paths
    pretty_print(path_and_status)

    while True:
        # while in the loop, scan the filepaths again (new_paths) for a delta comparison
        new_paths = scan_filepaths(req_path)

        if paths == new_paths:
            time.sleep(0.1)

        else:
            time.sleep(1.5) # whoa theres a difference, lets pause a bit, then scan again
            new_paths = scan_filepaths(req_path)
            path_and_status = update_path_and_statuses(path_and_status, paths, new_paths)
            paths = new_paths
            pretty_print(path_and_status)

if __name__ == "__main__":
    #main function, wrapped in a try to catch Ctrl + C keyboard exception (while sleeping)
    try:
        main()
    except KeyboardInterrupt: # sleep throws this exception if we Ctrl + C
        sys.exit(0)