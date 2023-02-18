This is a self-compiling diagram compiler.

It compiles diagrams created by the yEd diagram editor.

It runs under Linux (Ubuntu).

yEd must be installed https://www.yworks.com/products/yed/download.
SBCL must be installed (sudo apt-get install sbcl).
Buildapp must be installed (sudo apt-get install buildapp).
Quicklisp must be installed (https://www.quicklisp.org/beta/)
Gnu prolog must be installed (sudo apt-get install gprolog).

This compiler uses a lisp front-end to "scan" the .graphml file produced by yEd and to convert it a factbase, suitable for use with gprolog.

Then, several (8) passes are made over the factbase in a pipeline of gprolog commands.  Each pass augments the factbase with new information.

The result is a .gsh file (graph shell) in human-readable format.  The grash assembler reads the .gsh file and "interprets" it as a set of Linux pipe commands.  Each command gets its own forked process.  Each forked process takes input from stdin and produces output to stdout.  All of the forked processes run in parallel (concurrently) under the Linux kernel.

The compiler is run by the ./grun shell script.

The .gsh file in assembled and run by the ./run script.

The input to the compiler is the file `1.txt`.  This file is created by the plscan command, which is compiled from two lisp files - plscan.lisp and io.lisp.  The plscan command simply does some text rewriting from .graphml format to .pro format.  Graphml is a XML format that describes elements found on the diagram.

At present, the ./grun script outputs to a series of text files fb1.pro ... fb8.pro.  The final output is the file fb9.gsh.  This file contains the grash assembler commands that run the compiler by calling executable binaries for each pass (the names of the binaries are derived from the diagram pl_vsh.graphml)

The ./run shell script runs the compiler (again) to self-compile the diagram to a new file called `self.gsh`.  The intent is to `diff` the file `fb9.gsh` against the self-compiled file `self.gsh`.  There should be no differences if everything is working correctly.

A variation on this theme can be found in ../cl_vsh, where Common Lisp is used instead of Gnu PROLOG.  You can see that there is nothing magical about executing pattern matches against a factbase, except that the syntax of PROLOG makes it easier to write and to understand what was written.