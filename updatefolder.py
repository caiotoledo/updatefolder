import sys
import os
import fnmatch
import hashlib
from shutil import copyfile


def helpfunc():
    print("usage: compareFolder.py [FolderWithNewFiles] [FolderWithOldFiles]")


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


def get_file_hash256(myfile):
    sha256 = hashlib.sha256()
    with open(myfile, 'rb') as f:
        while True:
            data = f.read()
            if not data:
                break
            sha256.update(data)
        return sha256.hexdigest()


if len(sys.argv) < 3:
    helpfunc()
    sys.exit(1)

if check_path(sys.argv[1]) is False or check_path(sys.argv[2]) is False:
    print("usage: compareFolder.py [FolderWithNewFiles] [FolderWithOldFiles]")
    print("Arguments must be a valid path!")
    sys.exit(1)

updatedDir = sys.argv[1]
newDir = sys.argv[2]

for subdir, dirs, files in os.walk(updatedDir):
    filesNotFound = []
    for file in files:
        updatedFile = os.path.join(subdir, file)
        findFiles = find_pattern(file, newDir)
        if len(findFiles) > 0:
            shaFirst = get_file_hash256(updatedFile)
            for f in findFiles:
                shaSecond = get_file_hash256(f)
                if shaFirst != shaSecond:
                    copyfile(updatedFile, f)
                    print("Updated file:")
                    print(updatedFile, "->", f)
                    print("\n")
        else:
            filesNotFound.append(updatedFile)

if len(filesNotFound) > 0:
    print("FILES NOT FOUND:")
    for f in filesNotFound:
        print(f)
