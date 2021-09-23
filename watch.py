import os, sys, re, time

def full_path(path):
    """fixes /'s and used to expand an initial path component ~ to user’s home directory"""
    full_path = str(os.path.expanduser(path)).replace("/","\\")

    return full_path

def get_filepaths(path):
    filepaths = []

    for root, dirs, files in os.walk(path):
        for file in files:
            filepaths.append(os.path.join(root,file))

    return filepaths

def print_filepaths(req_path, filepaths):
    for filepath in filepaths:
        pretty_path = filepath[len(req_path):]
        print(pretty_path)

    return None

def main():
    try:
        while True:
            os.system("cls")

            if (len(sys.argv) > 1):
                req_path = full_path(sys.argv[1])
            else:
                req_path = full_path(os.getcwd())

            filepaths = get_filepaths(req_path)
            print_filepaths(req_path, filepaths)

            while True:
                time.sleep(0.25)
                if (filepaths == get_filepaths(req_path)):
                    None
                else:
                    break

    except KeyboardInterrupt: # sleep throws this exception if we ctrl+c
        sys.exit(0)

if __name__ == "__main__":
    main()