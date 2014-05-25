
SOURCES = \
	*.java

new:
	make clean
	make rc

debug:
	make clean
	make rcdbg

rc: $(SOURCES) parser.java sym.java
	javac RC.java
	cp RC.sh RC
	chmod 755 RC

rcdbg: $(SOURCES) parser.java sym.java
	javac RCdbg.java
	cp RCdbg.sh RC
	chmod 755 RC

parser.java: rc.cup
	javacup < rc.cup

clean:
	rm -f *.class RC parser.java sym.java a.out core rc.s

tar:
	tar cvf rc.tar $(SOURCES) Makefile RC.sh

#       Makes a backup called backups/MMDDMM:SS.tar.Z
backup:
	-@make clean
	-@mkdir backups
	tar cvf - $(SOURCES) Makefile RC.sh | compress > backups/`date +%m%d%R`.tar.Z
