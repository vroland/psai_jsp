#!/bin/python3

import sys
from collections import namedtuple,defaultdict

Operation = namedtuple("Operation", ["job_id", "op_id", "machine", "start", "end"])

import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import os
import select

plt.ion()
plt.show()

def schedule_from_lines(lines):
    """allocate operations to machines and parse input"""

    schedule = defaultdict(list)
    for job, line in enumerate(lines):
        for op, op_string in enumerate(line):
            start, end, machine = map(int, op_string.split(","))
            op_ex = Operation(job_id=job, op_id=op, start=start, end=end, machine=machine)
            schedule[machine].append(op_ex)

    return [schedule[k] for k in sorted(schedule.keys())]

def show_schedule(schedule):
    for m_ops in schedule:
        m_ops.sort(key=lambda o: o.start)

    max_job = max( [ max([op.job_id for op in slot]) for slot in schedule] )
    for slot in zip(*schedule):
        m_ops = list(slot)
        start = [op.start for op in m_ops]
        width = [op.end - op.start for op in m_ops]
        colors = [hsv_to_rgb((1.0 * op.job_id / (max_job + 1), 1, .85)) for op in m_ops]
        plt.barh(range(len(schedule)),  width, left=start, color=colors)

    plt.yticks(range(len(schedule)))
    plt.draw()
    plt.pause(0.001)

while True:
    lines = []

    data = b""
    while True:

        plt.pause(0.001)
        r, w, e = select.select([ sys.stdin ], [], [], 0)
        if sys.stdin in r:
            data += os.read(sys.stdin.fileno(), 50)

        if b"\n" in data:
            nlindex = data.index(b"\n")
            line = data[:nlindex].decode("utf-8")
            data = data[nlindex + 1:]
        else:
            line = ""

        if line.startswith("m:"):
            lines.append(line[2:].split())
        elif line.startswith("---"):
            print ("new schedule!")
            schedule = schedule_from_lines(lines)
            show_schedule(schedule)
            break
