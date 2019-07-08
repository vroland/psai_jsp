#!/bin/bash
# This presentation needs `bat`, a program for fancy source file output.
# If you don't have bat, you can replace it with any pager (like `less`).

trap 'echo "Anyway, lets continue..."' INT

clear
read -p "Hi! We are Claas de Boer, Philipp Hanisch, Valentin Roland."
clear
read -p "We chose to encode the job-shop scheduling problem as a CSP using MiniZinc."
clear
read -p "One of our problem instances looks like this:"

make work/instance_la02_lower_none.mzn
bat work/instance_la02_lower_none.mzn -l Pascal

clear
read -p "And our problem instance like this:"

bat src/encoding.mzn -l Pascal

clear
read -p "Now let's see it in action:"

make solve_la02

clear
read -p "(keep this solution length in mind)"
clear
read -p "That's nice, we have a solution, but how can we see that it makes sense?"

make vis_la02

clear
read -p "For small instances, the solver can give us the optimal solution."

make vis_ft06

clear
read -p "For bigger instances, this would take a while..."

make vis_swv17

clear
read -p "For bigger instances, we can iteratively explore the bounds:"

make iterate_vis_la02
