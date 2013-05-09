infiles  := $(wildcard *.in)
outfiles := $(infiles:.in=.out)
pyfiles  := $(wildcard *.py)

all: $(outfiles)

%.out: %.in $(pyfiles)
	pypy $(pyfiles) $< > $@ || rm $@
