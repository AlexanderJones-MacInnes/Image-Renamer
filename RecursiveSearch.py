import os, sys

def DirectorySearch(path):
    print(f"---{path}---", file=sys.stderr)
    fileList = os.scandir(path)

    for file in fileList:

        #If found file is a directory also search that
        #But only if '/a' was passed as an input argument
        #Or unless 'searchAll' flag is otherwise somehow true
        if file.is_dir() and searchAll:
            DirectorySearch(file.path)

        else:
            print(file.path)
    print(f"---{path}---", file=sys.stderr)


argv = sys.argv

#Flag if the search should recursively run on found directories
try:
    if sys.argv[2] == "/a":
        searchAll = True
except:
        searchAll = False

path = sys.argv[1]
#Help text for command-line users
if path == "/help" or path == "help" or path == "-help":
    print("\nThis program searches through file folders and returns the contents to stdout.\n"
          "The first argument should be the path of the folder you want to search through.\n"
          "The following arguments can also be passed...\n\n"
          "/a   Will cause the program to also search though any additional folders it finds in the search")

#Actual use-case in which argv[1] is a file path
else:
    DirectorySearch(path)