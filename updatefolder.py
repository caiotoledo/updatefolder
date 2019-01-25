import sys
import os
import fnmatch
import filecmp
from shutil import copyfile
import difflib


# Function to show script help
def helpfunc():
    print("usage: updatefolder.py [FolderWithNewFiles] [FolderWithOldFiles] [FilePattern]")
    print("FolderWithNewFiles: Folder with new Files to update the old folder")
    print("FolderWithOldFiles: Folder to be updated")
    print("FilePattern: File pattern to be updated, ex: *.txt")
    print("[OPTIONAL] IgnorePath: Path to be ignored during update")


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
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


str_ignore_diff = {
    "!!IGNORE-LINE!!",
    "GENERATION TIME :",
    "GENERATED ON:"
}


def has_ignore_diff(str):
    for s in str_ignore_diff:
        if str.find(s) != -1:
            return True
    if str.find(" * ") == 0:
        return True
    return False


def is_ignoreline_only_diff(file1, file2):
    ret = True
    lines1 = open(file1).readlines()
    lines2 = open(file2).readlines()
    diff = difflib.ndiff(lines1, lines2)
    deltas = ''.join(x[2:] for x in diff if x.startswith('- ')).split('\n')
    for l in deltas:
        if has_ignore_diff(l) is False and \
                len(l) > 0:
            ret = False
            break
    return ret


# Check number of arguments are valid
if len(sys.argv) != 4 and len(sys.argv) != 5:
    print("Wrong number of parameters!")
    helpfunc()
    sys.exit(1)

# Check if the path arguments is valid
if check_path(sys.argv[1]) is False or check_path(sys.argv[2]) is False:
    print("Folder arguments must be a valid path!")
    helpfunc()
    sys.exit(1)

# Store arg in variables
updatedDir = sys.argv[1]
newDir = sys.argv[2]
FilePattern = sys.argv[3]

# Check if "IgnorePath" is used
if len(sys.argv) == 5:
    IgnoreDir = sys.argv[4]
    if check_path(sys.argv[4]) is False:
        print("Folder arguments must be a valid path!")
        helpfunc()
        sys.exit(1)
else:
    IgnoreDir = ""


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

                        # Workaround to ignore generated source and header files by Tresos:
                        if fnmatch.fnmatch(updatedFile, "*.c") or fnmatch.fnmatch(updatedFile, "*.h"):
                            if is_ignoreline_only_diff(updatedFile, f) is True:
                                continue

                        copyfile(updatedFile, f)
                        print("Updated file:")
                        print(updatedFile, "->", f)
                        print("\n")
            else:
                filesNotFound.append(updatedFile)

if len(filesNotFound) > 0:
    print("FILES NOT FOUND ON", newDir, ":")
    for f in filesNotFound:
        print(f)
