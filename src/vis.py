#!python3

import sys


import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import os
import select
from mzn_instance import schedule_from_lines, Operation

plt.ion()
plt.show()

def show_schedule(schedule):
    for m_ops in schedule:
        m_ops.sort(key=lambda o: o.start)

    # clear axis
    plt.cla()
    # clear figure
    plt.clf()

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


data = b""
while True:
    lines = []

    while True:

        plt.pause(0.001)
        r, w, e = select.select([ sys.stdin ], [], [], 0)
        if sys.stdin in r:
            data += os.read(sys.stdin.fileno(), 50)

        if b"\n" in data:
            nlindex = data.index(b"\n")
            line = data[:nlindex].decode("utf-8")
            data = data[nlindex + 1:]
            print (line)
            sys.stdout.flush()
        else:
            line = ""

        if line.startswith("m:"):
            lines.append(line[2:].split())
        elif line.startswith("---"):
            schedule = schedule_from_lines(lines)
            show_schedule(schedule)
            break
