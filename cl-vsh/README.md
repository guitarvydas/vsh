This directory contains a version of the diagram compiler.

All of the work is done using an imperative language, in this case Common Lisp.

The compiler inputs a diagram created by the yEd editor and outputs a .gsh file (Graph assembler).

In this case the diagram is called `self.graphml`.

The compiler consists of 9 passes.

These passes are compiled and moved to ~/bin by `make`.

Each pass operates a little bit on the factbase, augments the factbase and passes the augmented factbase on down the line to the next pass.

The very first pass converts .graphml (XML) into a flat factbase format of triples, using the `xmls` library.  The rest of the passes use the factbase and add facts to the factbase as they inference bits of information about the diagram.

The final result is written to the file `self.grash` by the emit-grash pass.

The compiler is run by `./run-bootstrap`.

