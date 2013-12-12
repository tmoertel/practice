ins = $(wildcard *.in)
outs = $(ins:in=out)

default: $(outs)

%.out : %.in Tongues.hs
	runhaskell Tongues.hs < $< > $@
