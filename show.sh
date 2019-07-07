#!/bin/bash

trap 'echo "Anyway, lets continue..."' INT

read -p "Hi! We are ..."
read -p "We Chose to encode the job-shop scheduling problem as a CSP using MiniZinc."
read -p "One of our problem instances looks like this:"

make work/instance_la02_lower_none.mzn
bat work/instance_la02_lower_none.mzn -l Pascal

read -p "And our problem instance like this:"

bat src/encoding.mzn -l Pascal

read -p "Now let's see it in action:"

make solve_la02

read -p "(keep this solution length in mind)"
read -p "That's nice, we have a solution, but is it correct?"

make vis_la02

read -p "For small instances, the solver can give us the optimal solution."

make vis_ft06

read -p "For bigger instances, this would take a while..."

make vis_swv17

read -p "For bigger instances, we can iteratively explore the bounds:"

make iterate_vis_la02

