#name pl_vsh.gsh
pipes 7
fork
  stdoutPipe 6
  exec1st pl_check_input
krof
fork
  stdinPipe 6
  stdoutPipe 5
  exec pl_calc_bounds
krof
fork
  stdinPipe 5
  stdoutPipe 4
  exec pl_mark_directions
krof
fork
  stdinPipe 4
  stdoutPipe 3
  exec pl_match_ports_to_components
krof
fork
  stdinPipe 3
  stdoutPipe 2
  exec pl_assign_pipe_numbers_to_inputs
krof
fork
  stdinPipe 2
  stdoutPipe 1
  exec pl_assign_pipe_numbers_to_outputs
krof
fork
  stdinPipe 1
  stdoutPipe 0
  exec pl_assign_fds
krof
fork
  stdinPipe 0
  exec pl_emit
krof
