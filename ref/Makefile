COMPILER=g++ -std=c++11
SRCS = $(wildcard *.cpp)

all:
	make clean
	make compile

compile: 
	for cpp in $(SRCS) ; do	\
		$(COMPILER) -o $$cpp.out -g $$cpp ;	\
	done
	
clean:
	rm -f *.out


