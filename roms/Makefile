MAKEFILES = $(shell find . -maxdepth 5 -type f -name Makefile)
SUBDIRS   = $(filter-out ./,$(dir $(MAKEFILES)))

all:
	for dir in $(SUBDIRS); do \
  	make -C $$dir clean; \
		make -C $$dir ; \
  done

clean:
	for dir in $(SUBDIRS); do \
  	make -C $$dir clean; \
  done
