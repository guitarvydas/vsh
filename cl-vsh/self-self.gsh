#name self.gsh
pipes 8
fork
stdoutPipe 0
exec1st scan
krof 

fork
stdinPipe 0
stdoutPipe 7
exec check-input
krof 

fork
stdinPipe 7
stdoutPipe 1
exec calc-bounds
krof 

fork
stdinPipe 1
stdoutPipe 2
exec mark-directions
krof 

fork
stdinPipe 2
stdoutPipe 3
exec match-ports-to-components
krof 

fork
stdinPipe 3
stdoutPipe 4
exec assign-pipe-numbers-to-inputs
krof 

fork
stdinPipe 4
stdoutPipe 5
exec assign-pipe-numbers-to-outputs
krof 

fork
stdinPipe 5
stdoutPipe 6
exec assign-fds
krof 

fork
stdinPipe 6
exec emit-grash
krof 

