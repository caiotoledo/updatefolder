import sys
import os
import fnmatch
import filecmp
from shutil import copyfile
import difflib


def helpfunc():
    print("usage: updatefolder.py [FolderWithNewFiles] [FolderWithOldFiles] [FilePattern]")
    print("FolderWithNewFiles: Folder with new Files to update the old folder")
    print("FolderWithOldFiles: Folder to be updated")
    print("FilePattern: File pattern to be updated, ex: *.txt")


def check_path(path):
    if os.path.exists(path):
        return True
    else:
        return False


def find_pattern(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def is_ignoreline_only_diff(file1, file2):
    ret = True
    lines1 = open(file1).readlines()
    lines2 = open(file2).readlines()
    diff = difflib.ndiff(lines1, lines2)
    deltas = ''.join(x[2:] for x in diff if x.startswith('- ')).split('\n')
    for l in deltas:
        if l.find("!!IGNORE-LINE!!") == -1 and len(l) > 0:
            ret = False
            break
    return ret


if len(sys.argv) < 4:
    helpfunc()
    sys.exit(1)

if check_path(sys.argv[1]) is False or check_path(sys.argv[2]) is False:
    print("usage: compareFolder.py [FolderWithNewFiles] [FolderWithOldFiles]")
    print("Arguments must be a valid path!")
    sys.exit(1)

updatedDir = sys.argv[1]
newDir = sys.argv[2]
FilePattern = sys.argv[3]

for subdir, dirs, files in os.walk(updatedDir):
    filesNotFound = []
    for file in files:
        if fnmatch.fnmatch(file, FilePattern):
            updatedFile = os.path.join(subdir, file)
            findFiles = find_pattern(file, newDir)
            if any(updatedFile in s for s in findFiles):
                findFiles.remove(updatedFile)
            if len(findFiles) > 0:
                for f in findFiles:
                    if filecmp.cmp(f, updatedFile) is False:

                        # Workaround for generated source and header files:
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
