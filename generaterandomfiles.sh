#!/bin/sh

generatefile(){
	< /dev/urandom tr -dc "\t\n [:alnum:]" | head -c1000 >> $1
}

rm -rf ./folders/
mkdir -p folders/testfolder1
mkdir -p folders/testfolder2

# folders/testfolder1 files:
generatefile folders/testfolder1/file1.h
generatefile folders/testfolder1/file2.h
generatefile folders/testfolder1/file3.h
generatefile folders/testfolder1/file4.h

echo "OPA !!IGNORE-LINE!!\n" >> folders/testfolder1/fileignore1.h

echo "OPA !!IGNORE-LINE!!\n" >> folders/testfolder1/file5.h
generatefile folders/testfolder1/file5.h

generatefile folders/testfolder1/file6.h

# folders/testfolder2 files:
generatefile folders/testfolder2/file1.h
generatefile folders/testfolder2/file2.h
# Create the same file to be ignore by updatefolder script
cp folders/testfolder1/file3.h folders/testfolder2/

# Create a file that has only a diff in the !!IGNORE-LINE!!, and should be ignored
cp folders/testfolder1/fileignore1.h folders/testfolder2/
sed -i 's/OPA/HEY/g' folders/testfolder2/fileignore1.h

# Generate a file that has the !!IGNORE-LINE!! plus other differences, should be updated
echo "HEY !!IGNORE-LINE!!\n" >> folders/testfolder2/file5.h
generatefile folders/testfolder2/file5.h

# Generate a file that has only decremental differences
cp folders/testfolder1/file6.h folders/testfolder2/file6.h
sed -i '$ d' folders/testfolder1/file6.h
