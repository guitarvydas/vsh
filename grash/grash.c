/*
;;; Copyright (c) 2012, Paul Tarvydas
;;; All rights reserved.

;;; Redistribution and use in source and binary forms, with or without
;;; modification, are permitted provided that the following conditions
;;; are met:

;;;    Redistributions of source code must retain the above copyright
;;;    notice, this list of conditions and the following disclaimer.

;;;    Redistributions in binary form must reproduce the above
;;;    copyright notice, this list of conditions and the following
;;;    disclaimer in the documentation and/or other materials provided
;;;    with the distribution.

;;; THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
;;; CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
;;; INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
;;; MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
;;; DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
;;; BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
;;; EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
;;; TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
;;; DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
;;; ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
;;; TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
;;; THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
;;; SUCH DAMAGE.
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <assert.h>
#include <sys/wait.h>


/*
  GRAph SHell - a Flow-Based Programming shell

  (See https://www.cs.rutgers.edu/~pxk/416/notes/c-tutorials/pipe.html 
  section "Creating a pipe between two child processes" for a explanation
  of how to use dup2, etc.).

  A *nix shell that reads scripts of simple commands that plumb
  commands together with a graph of pipes / sockets / etc.

  This shell is not intended for heavy human consumption, but as an assembler
  that interprets programs created by graphical Flow-Based Programming
  (FBP) tools.

  Commands to the interpreter

  comments: # as very first character in the line

  empty line

  pipes N : creates N pipes starting at index 0
  push N : push N as an arg to the next command (dup)
  dup N : dup2(pipes[TOS][TOS-1],N), pop TOS, pop TOS
          pipes[x][y] : x is old pipe #, y is 0 for read-end, 1 for write-end, etc.
          N is the new (child's) FD to be overwritten with the dup'ed pipe (0 for stdin, 1 for stdout, etc).
  stdinPipe N - shorthand for above ; dup2(pipes[N][0],0)
  stdoutPipe N - shorthand for above ; dup2(pipes[N][1],1)
  stderrPipe N - shorthand for above ; dup2(pipes[N][2],2)
  exec <args> : splits the args and calls execvp, after closing all pipes
  exec1st <args> : splits the args, appends args from the command line and calls execvp, after closing all pipes
  fork : forks a new process
         parent ignores all subsequent commands until krof is seen
  krof : signifies end of forked child section
         parent resumes processing commands
	 child (if not exec'ed) terminates

  redir N - overwrite FD slot N by contents of slot TOS, pop TOS (no pipes used, straight call to dup2())
*/

#define PIPEMAX 100
#define LINEMAX 1024
#define ARGVMAX 128
#define STACKMAX 2

#define READ_END 0
#define WRITE_END 1

int comment (char *line) {
  /* return 1 if line begins with # or is empty, otherwise 0 */
  return line[0] == '#' || line[0] == '\n' || line[0] == '\0';
}

char *parse (char *cmd, char *line) {
  /* if command matches, return pointer to first non-whitespace char of args */
  while (*cmd)
    if (*cmd++ != *line++)
      return NULL;
  while (*line == ' ') line++;
  return line;
}

int pipes[PIPEMAX-1][2];
int usedPipes[PIPEMAX-1];
int child;
#define MAIN 1
#define PARENT 2
#define CHILD 3
int state = MAIN;
int stack[STACKMAX];
int sp = 0;

void quit (char *m) {
  perror (m);
  exit (1);
}

void push (char *p) {
  assert (sp < STACKMAX);
  stack[sp++] = atoi(p);
}

int pop () {
  assert (sp > 0);
  return stack[--sp];
}

void gclose (char *p) {
  int i = atoi(p);
  close(pipes[i][0]);
  close(pipes[i][1]);
}

void gdup (char *p) {
  int fd = atoi(p);
  int i = pop();
  int dir = pop();
  int oppositeDir = ((dir == READ_END) ? WRITE_END : READ_END);
  dup2 (pipes[i][dir], fd);
  close(pipes[i][oppositeDir]);  // flows are one-way only
  usedPipes[i] = 1;
}

void redirect (char *p) {
  int fd_slot_to_overwrite = atoi(p);
  int fd_slot_from = pop();
  fprintf (stderr, "dup2(%d,%d)\n", fd_slot_from, fd_slot_to_overwrite);
  dup2 (fd_slot_from, fd_slot_to_overwrite);
}

void gdup_std (char *p, int fd, int dir) {
  int i = atoi(p);
  int oppositeDir = ((dir == READ_END) ? WRITE_END : READ_END);
  dup2 (pipes[i][dir], fd);
  close(pipes[i][oppositeDir]);  // flows are one-way only
  usedPipes[i] = 1;
}

void gdup_stdin (char *p) {
  gdup_std (p, 0, READ_END);
}

void gdup_stdout (char *p) {
  gdup_std (p, 1, WRITE_END);
}

void gdup_stderr(char *p) {
  gdup_std (p, 2, WRITE_END);
}


int highPipe = -1;

void mkPipes (char *p) {
  int i = atoi(p);
  if (i <= 0 || i > PIPEMAX)
    quit("socket index");
  highPipe = i - 1;
  i = 0;
  while (i <= highPipe)
    if (pipe (pipes[i++]) < 0)
      quit ("error opening pipe pair");
}

void closeAllPipes () {
  // close all pipes in pipe array owned by the parent
  int i;
  for (i = 0 ; i <= highPipe ; i++) {
    close (pipes[i][READ_END]);
    close (pipes[i][WRITE_END]);
  }
}
	   
void closeUnusedPipes () {
  int i;
  for (i = 0 ; i <= highPipe ; i++) {
    if (usedPipes[i] == 0) {
      close (pipes[i][READ_END]);
      close (pipes[i][WRITE_END]);
    }
  }
}
	   

void doFork () {
  if ((child = fork()) == -1)
    quit ("fork");
  state = (child == 0) ? PARENT : CHILD;
}

void doKrof () {
  state = MAIN;
}

char *trim_white_space(char *p) {
  while (*p == ' ' || *p == '\t' || *p == '\n') {
    *p++ = '\0';
  }
  return p;
}

void  parseArgs(char *line, int *argc, char **argv) {
  /* convert the char line into argc/argv */
  *argc = 0;
  while (*line != '\0') {
    line = trim_white_space(line);
    if (*line == '\0') {
      break;
    }
    *argv++ = line;
    *argc += 1;
    while (*line != '\0' && *line != ' ' && 
	   *line != '\t' && *line != '\n') 
      line++;
  }
  *argv = NULL;
}
  
void appendArgs (int *argc, char **argv, int oargc, char **oargv) {
  /* tack extra command-line args onto tail of argv, using pointer copies */
  fprintf (stderr, "oargc=%d\n", oargc);
  fflush (stderr);
  if (oargc > 2) {
    int i = 2;
    while (i < oargc) {
      argv[*argc] = oargv[i];
      *argc += 1;
      i += 1;
    }
    argv[i] = NULL;
  }
}

void doExec (char *p, int oargc, char **oargv, int first) {
  char *argv[ARGVMAX];
  int argc;
  pid_t pid;
  int i;
  parseArgs (p, &argc, argv);
  if (first) {
    appendArgs (&argc, argv, oargc, oargv);
  }
  closeUnusedPipes();

  fprintf (stderr, "execing[%d]:", argc);
  fflush (stderr);
  for(i=0; i < argc; i+=1) {
    fprintf (stderr, " %s", argv[i]);
    fflush (stderr);
  }
  fprintf (stderr, "\n");
  fflush (stderr);

  pid = execvp (argv[0], argv);
  if (pid < 0) {
    fprintf (stderr, "exec: %s\n", argv[0]);
    quit ("exec failed!");
  }
}

void interpret (char *line, int argc, char **argv) {
  char *p;

  line = trim_white_space(line);

  if (comment (line))
    return;

  switch (state) {

  case CHILD:
    p = parse ("krof", line);
    if (p)
      exit(0);
    p = parse ("dup", line);
    if (p) {
      gdup (p);
      return;
    }
    p = parse ("stdinPipe", line);
    if (p) {
      gdup_stdin (p);
      return;
    }
    p = parse ("stdoutPipe", line);
    if (p) {
      gdup_stdout (p);
      return;
    } 
    p = parse ("stderrPipe", line);
    if (p) {
      gdup_stderr (p);
      return;
    }
    p = parse ("push", line);
    if (p) {
      push (p);
      return;
    }
    p = parse ("exec1st", line);
    if (p) {
      doExec (p, argc, argv, 1);
      return;
    }
    p = parse ("exec", line);
    if (p) {
      doExec (p, argc, argv, 0);
      return;
    }
    p = parse ("redir", line);
    if (p) {
      redirect (p);
      return;
    }
    quit("can't happen");
    break;

  case MAIN:
    p = parse ("pipes", line);
    if (p) {
      mkPipes (p);
      return;
    }
    p = parse ("fork", line);
    if (p) {
      doFork ();
      return;
    }
    p = parse ("krof", line);
    if (p)
      quit ("krof seen in MAIN state (can't happen)");
    break;

  case PARENT:
    p = parse ("krof", line);
    if (p) {
      doKrof ();
      return;
    }
    return;
  }
  quit ("command");
}
  

int main (int argc, char **argv) {
  int r;
  char line[LINEMAX-1];
  char *p;
  FILE *f;
  pid_t pid;
  int status;

  if (argc < 2 || argv[1][0] == '-') {
    f = stdin;
  } else {
    f = fopen (argv[1], "r");
  }
  if (f == NULL)
    quit ("usage: grash {filename|-} [args]");

  for (r = 0; r < PIPEMAX; r++) {
    pipes[r][READ_END] = -1;
    pipes[r][WRITE_END] = -1;
    usedPipes[r] = 0;
  }
  
  p = fgets (line, sizeof(line), f);
  while (p != NULL) {
    interpret (line, argc, argv);
    p = fgets (line, sizeof(line), f);
  }
  closeAllPipes();
  while ((pid = wait(&status)) != -1) {
    fprintf(stderr, "%d exits %d\n", pid, WEXITSTATUS(status));
  }
  exit(0);
}
