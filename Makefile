FILES = lab3b.py Makefile README lab3b.sh
.SILENT:

default: build

build:
	cp lab3b.sh lab3b
	chmod +x lab3b
	echo "build success" > /dev/null

clean:
	rm -f *.o *~ *.tar.gz lab3b

dist: clean
	tar -czvf lab3b-604626024.tar.gz ${FILES}
