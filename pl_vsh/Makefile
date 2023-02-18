PATH=/usr/local/bin/:~/bin/:$PATH
bindir = ~/bin

execs =  $(bindir)/plscan

all : $(execs) io.lisp

$(bindir)/% : %.lisp io.lisp
	rm -f $@
	buildapp --output $@  --load $< --entry main

clean:
	rm -f $(execs)
