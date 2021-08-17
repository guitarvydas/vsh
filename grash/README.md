Grash (GRAphical SHell) is a small C program (approx. 250 lines) that works like /bin/bash but has most of the features stripped out.  Grash only creates forks and execs named programs.

The commands are:
- # empty line
- pipes N
- push N
- dup N
- exec <args>
- exec1st <args>
- fork
- krof

See `dup2 doc.drawio` if you want to know how this works.

See `../cl-vsh/vsh.gsh` for an example of a grash file (which happens to be the compiler itself).

Documentation from grash.c:
``` 
  empty line

  pipes N : creates N pipes starting at index 0
  push N : push N as an arg to the next command (dup)
  dup N : dup2(pipes[TOS][TOS-1],N), pop TOS, pop TOS
          pipes[x][y] : x is old pipe #, y is 0 for read-end, 1 for write-end, etc.
          N is the new (child's) FD to be overwritten with the dup'ed pipe (0 for stdin, 1 for stdout, etc).
  exec <args> : splits the args and calls execvp, after closing all pipes
  exec1st <args> : splits the args, appends args from the command line and calls execvp, after closing all pipes
  fork : forks a new process
         parent ignores all subsequent commands until krof is seen
  krof : signifies end of forked child section
         parent resumes processing commands
	 child (if not exec'ed) terminates
```

to build:
- see makefile
- see grash.c
