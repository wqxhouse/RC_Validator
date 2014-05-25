CC=cc
SRCS = $(wildcard *.rc.s)

all:
	make clean
	make compile

compile: 
	for asm in $(SRCS) ; do	\
		$(CC) -o $$asm.out -g $$asm input.c output.s $(LINKOBJ) ;	\
	done
	
clean:
	rm -f *.rc.s.out


