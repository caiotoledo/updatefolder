import os
import sys
from collections import OrderedDict

# ------------------------------------------------------------------
# command configurations
# ------------------------------------------------------------------
CONFIG = {
    "update_folder" : [
        {
            "bin":"python scripts/updatefolder.py",
            "params": OrderedDict([
                ("%s/rte-%s-AutosarOs/TresosWs/%s", ["dir_build", "variant", "variant"]),
                (folderOld, ["dir_root"]),
                (parttern,  []),
                ("%s/rte-%s-AutosarOs/TresosWs/%s/virginimport", ["dir_build", "variant", "variant"])
            ])
        } for parttern, folderOld in [
            ("*.xdm", "%s/adapt/"),
            ("*.arxml", "%s/adapt/"),
            ("*.arxml", "%s/pkg/application/"),
            ("*.xdm", "%s/pkg/application/")
        ]
    ] + [
        {
            "bin":"python scripts/updatefolder.py",
            "params": OrderedDict([
                ("%s/rte-%s-AutosarOs/TresosWs/%s/output/generated", ["dir_build", "variant", "variant"]),
                ("%s/pkg/application/", ["dir_root"]),
                (parttern, [])
            ])
        } for parttern in [ "*.c", "*.h" ]
    ]
}

def parse(cmd, params):
    ret = []
    for conf in CONFIG[cmd]:
        cmd = conf["bin"] + " "
        for p in conf["params"]:
            cmd += p % tuple([params[v] for v in conf["params"][p]])
            cmd += " "
        ret += [cmd]
    return ret

def execute(cmds):
    for cmd in cmds:
        os.system(cmd)

# Called from command line
lszArgVariant        = "*"
lszArgSelectionMode  = ""
lszArgCmds           = ""
lszArgRootDir        = ""
lszArgBuildDir       = ""
lszArgRepoDir        = ""

# Called from command line
# check the given arguments
for lszArgument in sys.argv:
    if (lszArgument.find(__file__)>=0):
        pass
    elif (lszArgument.find("-variant=")==0):
        lszArgument = lszArgument[len("-variant="):]
        lszArgVariant = lszArgument.strip()
    elif (lszArgument.find("-selectionmode=")==0):
        lszArgument = lszArgument[len("-selectionmode="):]
        lszArgSelectionMode = lszArgument.strip()
    elif (lszArgument.find("-root_dir=") == 0):
        lszArgument = lszArgument[len("-root_dir="):]
        lszArgRootDir = lszArgument.strip()
    elif (lszArgument.find("-build_dir=") == 0):
        lszArgument = lszArgument[len("-build_dir="):]
        lszArgBuildDir = lszArgument.strip()
    elif (lszArgument.find("-repo_dir=") == 0):
        lszArgument = lszArgument[len("-repo_dir="):]
        lszArgRepoDir = lszArgument.strip()
    elif (lszArgument.find("-cmds=") == 0):
        lszArgument = lszArgument[len("-cmds="):]
        lszArgCmds = lszArgument.strip()
    else:
        print(lszArgument)
        sys.exit(1)

dir_root  = os.path.abspath(os.path.join(os.getcwd(), lszArgRootDir))
dir_repo  = os.path.abspath(os.path.join(dir_root, lszArgRepoDir))
dir_build = os.path.abspath(os.path.join(dir_root, lszArgBuildDir))

lszPythonPath = os.path.abspath(os.path.join(dir_repo, "scripts/python"))
# Load the scripts.
# Note: tcSystem is some case of base class to access the other classes. e.g. the class for variants handling (tcVariants)
sys.path.insert(0, lszPythonPath)
from PyClass_System import tcSystem
from PyClass_Log import tcLog
from PyClass_ErrorHandler import tcErrorHandler
from PyClass_FileHandler import tcFileHandler
from PyClass_Cmd import tcCmd

lcLog = tcLog(None, "w")
lcErr = tcErrorHandler(lcLog)

lcSystem = tcSystem(dir_root, dir_repo, dir_build, lcLog, lcErr)
lcCmd = tcCmd(lcLog, lcErr)

if not lcSystem.isValid():
    sys.exit(1)

lLstVariants = lcSystem.Variants_GetSelectionList(lszArgSelectionMode , lszArgVariant)

if (lLstVariants == None):
    lcErr.write(lszThisFile + ": ", 1, "No variant fits/given")
    sys.exit(1)
else:
    if len(lLstVariants) == 0:
        lcErr.write(lszThisFile + ": ", 1, "No variant fits/given")
        sys.exit(1)

for cmd in lszArgCmds.split(";"):
    for variant in lLstVariants:
        params = {
            "variant" : lcSystem.Variant_Load(variant).GetName(),
            "dir_root" : dir_root,
            "dir_build" : dir_build
        }
        execute(parse(cmd, params))
