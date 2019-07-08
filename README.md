JSP Scheduler
=============

Implements a job-shop scheduler as part of the practical work for the course [Problem Solving and Search in AI](https://iccl.inf.tu-dresden.de/web/Problem_Solving_and_Search_in_Artificial_Intelligence_\(SS2019\)).

Getting Started
---------------

First, make sure you have the following dependencies installed on your system:
- python 3.6 (for older versions, replace the f-string syntax)
- python3-matplotlib
- minizinc
- curl
- make

Then, set the path to the minizinc executable in `Makefile`:

```makefile
MINIZINC := path/to/minizinc
```

That's it!

Solving Instances
-----------------

This implementation can solve JSP instances in merged (combined operation time and machine) format. An example file will be downloaded if it is not present.

Three basic modes are suported:
- `solve_%`: Try to find an optimal solution for instance `%`.
- `vis_%`: Try to find an optimal solution, while showing the current best as a plot.
- `iterate_vis_%`: Try to find an optimal solution by iterative scaling scaling, while showing the current scaled upper bound schedule.

Examples:
- `make solve_ft06`
- `make vis_la02`
- `make vis_swv17`
- others in `show.sh`

Output Format
-------------

```
m:5,6,2 6,9,0 16,22,1 30,37,3 38,41,5 42,48,4
m:0,8,1 8,13,2 13,23,4 28,38,5 38,48,0 48,52,3
m:0,5,2 5,9,3 9,17,5 18,27,0 27,28,1 48,55,4
m:8,13,1 13,18,0 22,27,2 27,30,3 30,38,4 45,54,5
m:13,22,2 22,25,1 25,30,4 41,45,5 48,51,0 52,53,3
m:13,16,1 16,19,3 19,28,5 28,38,0 38,42,4 42,43,2
l:55
% time elapsed: 0.04 s
-----
```

A model is a collection of lines prefixed by `m:`, followed by `-----`.
Each line with the `m:`-prefix represents a job. Each job is a list of
space-separated 3-Tuples (`operation_start,operation_end,machine`), which represent the job's operations. See `src/encoding.mzn` for details.
