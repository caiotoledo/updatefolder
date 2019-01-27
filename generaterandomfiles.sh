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

# folders/testfolder2 files:
generatefile folders/testfolder2/file1.h
generatefile folders/testfolder2/file2.h
cp folders/testfolder1/file3.h folders/testfolder2/

cp folders/testfolder1/fileignore1.h folders/testfolder2/
sed -i 's/OPA/HEY/g' folders/testfolder2/fileignore1.h

echo "HEY !!IGNORE-LINE!!\n" >> folders/testfolder2/file5.h
generatefile folders/testfolder2/file5.h
