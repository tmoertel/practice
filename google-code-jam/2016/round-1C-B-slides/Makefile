ins = $(wildcard *.in)
outs = $(ins:in=out)
pybin = $(wildcard *.py)

default: $(outs)

%.out : %.in $(pybin)
	python $(pybin) $< > $@
