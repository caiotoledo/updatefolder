import sys
import os
import fnmatch
import filecmp
from shutil import copyfile
import difflib
import argparse

# Version variable:
__version__ = "v0.2.0"

# Arguments parser:
parser = argparse.ArgumentParser(description='Update a folder with new files')
parser.add_argument("--FolderWithNewFiles",
                    dest="FolderWithNewFiles",
                    help="Folder with new Files to update the old folder",
                    metavar="NEWFOLDER",
                    required=True)
parser.add_argument("--FolderWithOldFiles",
                    dest="FolderWithOldFiles",
                    help="Folder to be updated",
                    metavar="OLDFOLDER",
                    required=True)
parser.add_argument("--FilePattern",
                    dest="FilePattern",
                    help="File pattern to be updated, ex: *.txt",
                    metavar="PATTERNFILE",
                    required=True)
parser.add_argument("--IgnorePath",
                    dest="IgnorePath",
                    help="[OPTIONAL] Path to be ignored during update",
                    metavar="IGNOREPATH",
                    default='')
parser.add_argument("--IgnoreString",
                    dest="IgnoreString",
                    help="[OPTIONAL] If the diff contains only theses strings, it will be ignored",
                    metavar="IGNORESTR",
                    nargs="+")
parser.add_argument("--version",
                    action='version',
                    version=__version__)
args = parser.parse_args()


# Verify if its a existent path
def check_path(path):
    if os.path.exists(path):
        return True
    else:
        return False


# Find all files that matches with a given pattern
def find_pattern(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        _ = dirs
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def has_ignore_diff(str, str_ignore_diff=None):
    if str_ignore_diff is not None:
        for s in str_ignore_diff:
            if str.find(s) != -1:
                return True
    # Ignore comments changes:
    if str.find(" * ") == 0:
        return True
    return False


def is_ignoreline_only_diff(file1, file2):
    ret = True
    lines1 = open(file1).readlines()
    lines2 = open(file2).readlines()
    diff1 = difflib.ndiff(lines1, lines2)
    diff2 = difflib.ndiff(lines2, lines1)
    deltas = ''.join(x[2:] for x in diff1 if x.startswith('- ')).split('\n')
    deltas += ''.join(x[2:] for x in diff2 if x.startswith('- ')).split('\n')
    for l in deltas:
        if has_ignore_diff(l,args.IgnoreString) is False and \
                len(l) > 0:
            ret = False
            break
    return ret


# Store arg in variables
updatedDir = args.FolderWithNewFiles
newDir = args.FolderWithOldFiles
FilePattern = args.FilePattern
IgnoreDir = args.IgnorePath

# Check if the path arguments is valid
if check_path(updatedDir) is False or check_path(updatedDir) is False:
    print("Folder arguments must be a valid path!")
    parser.print_help()
    sys.exit(1)

# Check if "IgnorePath" is used
if len(IgnoreDir) > 0:
    if check_path(IgnoreDir) is False:
        print("Folder arguments must be a valid path!")
        sys.exit(1)


filesNotFound = []
for subdir, dirs, files in os.walk(updatedDir):
    for file in files:
        if fnmatch.fnmatch(file, FilePattern):
            updatedFile = os.path.join(subdir, file)
            findFiles = find_pattern(file, newDir)

            # Do not update files in "IgnorePath"
            if os.path.normpath(IgnoreDir) in os.path.normpath(updatedFile) and len(IgnoreDir) > 0:
                continue

            # Remove files found in UpdatedDir:
            removeFiles = []
            for f in findFiles:
                if updatedDir in f:
                    removeFiles.append(f)
            for f in removeFiles:
                findFiles.remove(f)

            if len(findFiles) > 0:
                for f in findFiles:
                    if filecmp.cmp(f, updatedFile) is False:

                        if is_ignoreline_only_diff(updatedFile, f) is True:
                            continue

                        copyfile(updatedFile, f)
                        print("Updated file:")
                        print(updatedFile + " -> " + f)
                        print("\n")
            else:
                filesNotFound.append(updatedFile)

if len(filesNotFound) > 0:
    print("FILES NOT FOUND ON " + newDir + ":")
    for f in filesNotFound:
        print(f)
