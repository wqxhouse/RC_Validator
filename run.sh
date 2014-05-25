#!/bin/bash
RCFILES="self/*.rc"
CPPFILES="self/*.cpp"

echo "========================= generating self rc.s"
cd self
rm -f *.out
rm -f *.rc.s
./purifydos.sh
cd ..

for rcfile in $RCFILES; do
	cd src
	echo ${rcfile%%.*}
	./RC "../$rcfile"
	mv rc.s ../$rcfile.s
	cd ..
done

echo "========================= generating self binaries"
cd self
make
cd ..

echo "========================= converting rc to cpp"
cd self
../pythonDir/python convert.py
cd ..

echo "========================= moving all cpp to /ref"
cd ref
rm -f *.cpp
rm -f *.out
cd ..

for cppfile in $CPPFILES; do
	mv $cppfile ref
done

echo "========================= generating cpp binaries for comparison"
cd ref
make
cd ..

echo "========================= clearing tmp and res folder"
cd tmp
rm -f *.txt
cd ..

cd res
rm -f *.txt
cd ..

echo "========================= generating and diff results"
cd self
for binary in *.out; do
	filename=${binary%%.*};
	#echo $filename;
	./$binary > ../tmp/s_$filename.txt
	../ref/$filename.rc.cpp.out > ../tmp/c_$filename.txt
	diff ../tmp/s_$filename.txt ../tmp/c_$filename.txt > ../res/r_$filename.txt
done

