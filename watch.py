"""watch a given directory for file changes using the command line, useful for demos"""
import os, platform, sys, time, argparse, math, logging
from colour import Colour

def normalised_path(input_path:str) -> str:
    """returns a normalised "real"/"full" filepath for a given directory then checks its a valid directory"""
    normalised_path:str = os.path.realpath(os.path.expanduser(input_path)) + "\\"
    if os.path.isdir(normalised_path):
        return normalised_path
    else:
        raise NotADirectoryError("Not a Valid Directory")

def get_list_of_paths(given_directory:list, include_dirs:bool = True) -> list:
    """returns a list of paths inside a given directory, optionally includes folders"""
    paths:list = []
    for root, dirs, files in os.walk(given_directory):
        for file in files:
            filepath = os.path.join(root,file)
            paths.append(filepath[len(given_directory):]) # slice to remove root dir
        if include_dirs: # only apparen directories to the list if flag is true
            for dir in dirs:
                filepath = os.path.join(root,dir)
                paths.append(filepath[len(given_directory):] + "\\") # slice to remove root dir
    paths.sort() # sorts alphabetically
    return paths

class Status:
    SAME:str = "Same"
    ADDED:str = "Added"
    REMOVED:str = "Removed"
    DEAD:str = "Dead"

def create_path_to_status_dict(paths:list) -> dict:
    """returns a dictionary with a list of paths (keys) and all statuses (values) set to SAME"""
    path_to_status_dict:dict = {}
    for path in paths:
        path_to_status_dict[path] = Status.SAME

    path_to_status_dict = dict(sorted(path_to_status_dict.items())) # sort alphabetically
    return path_to_status_dict

def update_path_to_status_dict(path_to_status_dict:dict, new_paths:list) -> dict:
    """returns (updates) the path_to_status_dict, adds new paths and changes status for each path"""
    # set everything in the dictionary to removed or dead, after this we'll bring new in and no-change things back
    for path in path_to_status_dict:
        if path_to_status_dict[path] == Status.REMOVED or path_to_status_dict[path] == Status.DEAD:
            path_to_status_dict[path] = Status.DEAD
        elif path_to_status_dict[path] == Status.SAME or path_to_status_dict[path] == Status.ADDED:
            path_to_status_dict[path] = Status.REMOVED

    for np in new_paths:
        if np in path_to_status_dict.keys() and path_to_status_dict[np] != Status.DEAD:
            path_to_status_dict[np] = Status.SAME
        else:
            path_to_status_dict[np] = Status.ADDED

    path_to_status_dict = dict(sorted(path_to_status_dict.items())) # sort alphabetically
    return path_to_status_dict

def flush_path_to_status_dict(path_to_status_dict:dict) -> dict:
    """flushes the path_to_status_dict, cleans up removes and changes adds to no change"""
    # set everything in the dictionary to removed or dead, after this we'll bring new in and no-change things back
    for path in path_to_status_dict:
        if path_to_status_dict[path] == Status.REMOVED or path_to_status_dict[path] == Status.DEAD:
            path_to_status_dict[path] = Status.DEAD
        elif path_to_status_dict[path] == Status.SAME or path_to_status_dict[path] == Status.ADDED:
            path_to_status_dict[path] = Status.SAME

    path_to_status_dict = dict(sorted(path_to_status_dict.items())) # sort alphabetically
    return path_to_status_dict

def clear_the_screen() -> None:
    if(platform.system().lower()=="windows"):
        os.system("cls")
    else:
        os.system("clear")
    return None

def write_paths_to_screen(path_to_status_dict, show_dead:bool = False, clear_screen:bool = False, use_colours:bool = True) -> None:
    """write the path_to_status_dict to screen, one line per path and colour=status"""
    # Clear the screen
    if clear_screen:
        clear_the_screen() # platform indepedance

    for path, status in path_to_status_dict.items():
        if use_colours:
            colour = Colour() # initialise a colour object, this will allow us to print in colour
            if status == Status.SAME:
                print(path)
            elif status == Status.ADDED:
                colour.print(path,Colour.GREEN)
            elif status == Status.REMOVED:
                colour.print(path,Colour.RED)
            elif status == Status.DEAD and show_dead:
                colour.print(path,Colour.GRAY)
        else: # no colour, so just print files we care about
            if status == Status.SAME or status == Status.ADDED:
                print(path)
    logging.debug(str(path_to_status_dict))
    return None

def main() -> None:
    """main function, prints out the file paths, then starts a loop to check changes before printing"""
    # setup argparse to accept path, verbose flag and tick float
    parser = argparse.ArgumentParser()
    parser.add_argument('path',
                        nargs='?',
                        type=normalised_path, # cleanup the input path, expand if required, finish with "/"
                        default=os.getcwd()+"\\", # use the current working directory as a default
                        help='path to watch, otherwise use working directory'
                        )
    parser.add_argument('-k', '--keep',
                        action='store_true',
                        dest='keep', #bool
                        help='keep deleted files on-screen'
                        )
    parser.add_argument('-t', '--tick',
                        dest='tick',
                        type=float,
                        default=1.5, #default tick is 1.5 seconds, enough time for a 'git init'
                        help='time we\'ll wait to print directory out after a change'
                        )
    parser.add_argument('-o', '--omit-dirs',
                        action='store_true',
                        dest='omit_dirs', #bool
                        help='hide directories from the output (default behaviour is show)'
                        )
    parser.add_argument('-c', '--colourless',
                        action='store_true',
                        dest='colourless', #bool
                        help='disable the colour rendering and file removal delay'
                        )
    args = parser.parse_args()

    # flags store as true, we'll flip them to make them symantically useful
    is_colour:bool = not args.colourless
    show_dirs:bool = not args.omit_dirs

    # debug flags info
    logging.info("path:\t\t" + str(args.path))
    logging.info("keep:\t\t" + str(args.keep))
    logging.info("tick:\t\t" + str(args.tick))
    logging.info("colour:\t\t" + str(is_colour))
    logging.info("dirs:\t\t" + str(show_dirs))

    # set the window title
    os.system("title watching " + args.path.lower())

    # setup timer/tickers
    wait:float = math.floor(args.tick)/10 # tenth of a rounded down tick ( e.g. floor(1.5) == 1.0 )
    logging.info("wait_nc:\t" + str(wait))

    # grab all the file/folder paths under "path" and define valid statuses
    paths:list = get_list_of_paths(args.path, show_dirs)
    logging.info("paths:\t\t" + str(paths)[:250] + "...")

    # initialise the core dictionary mapping paths to statuses
    path_to_status_dict:dict = create_path_to_status_dict(paths) # key is "path", value is "status"
    logging.info("p_2_s_d:\t" + str(path_to_status_dict)[:250] + "...")

    # fresh flag used to check if changes to the list are shown in colour
    show_changes_counter:int = 30 # stops flash on start
    logging.info("shw_ch:\t\t" + str(show_changes_counter))

    # pretty print (optional clear screen and colours) the list of paths
    write_paths_to_screen(path_to_status_dict, args.keep, True, is_colour)

    # start an infinite loop printing the paths to screen
    while True:

        # do nothing, we're waiting for a change to happen in the directory, default is 0.1 second
        time.sleep(wait)

        # check for a change
        if paths != get_list_of_paths(args.path, show_dirs):
            time.sleep(args.tick) # change, sleep for the tick for any changes to finish
            paths = get_list_of_paths(args.path, show_dirs)
            path_to_status_dict = update_path_to_status_dict(path_to_status_dict, paths)
            write_paths_to_screen(path_to_status_dict, args.keep, True, is_colour)
            if is_colour: # for colour apps we reset the timer ready to refresh, colourless is static
                show_changes_counter = 0

        else:
            if show_changes_counter <= 30:
                show_changes_counter += 1
            if show_changes_counter == 30:
                path_to_status_dict = flush_path_to_status_dict(path_to_status_dict)
                write_paths_to_screen(path_to_status_dict, args.keep, True, is_colour)

if __name__ == "__main__":
    logging.basicConfig(format='%(message)s', level=logging.ERROR)
    #main function, wrapped in a try to catch Ctrl + C keyboard exception (while sleeping)
    try:
        main()
    except KeyboardInterrupt: # sleep throws this exception if we Ctrl + C
        sys.exit(0)