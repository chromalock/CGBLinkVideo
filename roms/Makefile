MAKEFILES = $(shell find . -maxdepth 5 -type f -name Makefile)
SUBDIRS   = $(filter-out ./,$(dir $(MAKEFILES)))

all:
	for dir in $(SUBDIRS); do \
  	make -C $$dir clean; \
		make -C $$dir ; \
  done
	find . -name \*.gbc -exec cp -n {} out \;

clean:
	for dir in $(SUBDIRS); do \
  	make -C $$dir clean; \
  done
	rm -r ./out/*.gbc
