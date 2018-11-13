#!/bin/sh

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "Generating files..."
./generaterandomfiles.sh

echo -e "\n"
echo "Calling updatefolder.py:"
echo "python updatefolder.py ./folders/testfolder1 ./folders/ *.h"
python updatefolder.py ./folders/testfolder1 ./folders/ *.h

echo -e "\n"
echo "Running Test verification:"
cd folders/testfolder2/
error=0
for file in *; do
	ret=$(diff -I '!!IGNORE-LINE!!' ../../folders/testfolder1/$file $file)
	if [[ -n "${ret// }" ]]; then
		echo -e "${RED}ERROR in $file ${NC}"
		error=1
	fi
done
cd $PWD
if [ $error == 0 ]; then
	echo -e "${GREEN}NO ERRORS FOUND!${NC}"
else
	exit 1
fi
