#!/bin/bash
mkfifo pipe1
./hello.sample.bash 4>pipe1 &
hello_pid=$!
./world.sample.bash 3<pipe1 &
world_pid=$!
wait $hello_pid
wait $world_pid
