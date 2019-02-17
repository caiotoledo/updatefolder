#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "Generating files..."
./generaterandomfiles.sh

echo -e "\n"
echo "Current version:"
python3 updatefolder.py --version

echo -e "\n"
echo "Calling updatefolder.py:"
set -v
python3 updatefolder.py --FolderWithNewFiles ./folders/testfolder1 --FolderWithOldFiles ./folders/ --FilePattern *.h --IgnoreString '!!IGNORE-LINE!!' 'GENERATION TIME' 'GENERATED ON:'
set +v

echo -e "\n"
echo "Running Test verification:"
cd folders/testfolder2/
error=0
for file in *; do
	ret=$(diff -I '!!IGNORE-LINE!!' ../../folders/testfolder1/$file $file)
	if [ ! -z "$ret" ]; then
		echo -e "${RED}ERROR in $file ${NC}"
		error=1
	fi
done
cd ../../
rm -rf folders
if [ $error -eq 0 ]; then
	echo -e "${GREEN}NO ERRORS FOUND!${NC}"
fi
exit $error
