# Tom Moertel <tom@moertel.com>
#
# Makefile for building and testing my Haskell solutions to the
# problems of the 20th Annual ACM International Collegiate
# Programming Contents Finals.
#
# https://icpc.global/newcms/community/history-icpc-1996/1996WorldFinalProblemSet.pdf
#
# $Id: Makefile,v 1.9 2002/02/11 07:33:08 thor Exp $

WARN          = -Wall -fno-warn-missing-signatures
GHC_SPECIALS  = -fglasgow-exts -fallow-overlapping-instances
GHC_OPT_LEVEL = -O2
GHC_PKGS      = -package lang
GHC_OPTS      = $(WARN) $(GHC_SPECIALS) $(GHC_PKGS) $(GHC_OPT_LEVEL) -i.:FGL

SOURCES  := $(wildcard *.hs)
TARGETS  := $(SOURCES:.hs=)
INPUTS   := $(wildcard *.input)
OUTPUTS  := $(INPUTS:.input=.output)

all : test

help :
	@echo Available targets: all test clean $(TARGETS)

% : %.hs
	ghc --make $(GHC_OPTS) -o $@ $@

%.output : % %.input
	./$< < ${@:.output=.input} | tee $@

test : $(OUTPUTS) $(TARGETS)

clean :
	rm -f $(TARGETS) *.hi *.o *~

.PHONY : all test clean
