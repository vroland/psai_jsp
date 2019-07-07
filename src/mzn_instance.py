"""
Transform JSP instances to minizinc format.
"""

import sys
from parser import load_instances
from math import floor, ceil
from collections import defaultdict,namedtuple

Operation = namedtuple("Operation", ["job_id", "op_id", "machine", "start", "end"])

def mzn_instance(instance, scale, bounds):
    """
    Writes an instance, time scaled with function `scale`.
    `bounds` is a tuple of the time domain bounds (inclusive).
    """

    def range(name, to):
        return [
            "int: num_{} = {}".format(name, to),
            "set of int: {} = 1..num_{}".format(name.upper(), name)
        ]

    # ranges
    facts = range("jobs", len(instance.jobs))
    facts += range("machines", instance.num_machines)
    facts += range("operations", len(instance.jobs[0].operations))
    facts += [f"int: LOWER_BOUND = {scale(bounds[0])}"]
    facts += [f"int: UPPER_BOUND = {scale(bounds[1])}"]


    oplengths = []
    opmachines = []
    for job in instance.jobs:
        oplengths += ["{}|".format(", ".join([str(scale(op.time)) for op in job.operations]))]
        opmachines += ["{}|".format(", ".join([str(op.machine) for op in job.operations]))]

    facts += ["array[JOBS, OPERATIONS] of int: oplengths = [|\n{}]".format("\n".join(oplengths))]
    facts += ["array[JOBS, OPERATIONS] of int: opmachines = [|\n{}]".format("\n".join(opmachines))]
    return ";\n".join(facts)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='generate a minizinc instance')
    parser.add_argument('infile', help='a file to search for instances')
    parser.add_argument('instance', help='name of the instance to use')
    parser.add_argument('--scale', help='time scale factor', default=1, type=int)
    parser.add_argument('--upper', help='generate scaled upper bound instead of lower bound', default=False, action='store_true')
    parser.add_argument('--bounds', help='time domain bounds in format <lower>-<upper>', default=None)

    args = parser.parse_args()
    instances = load_instances(args.infile)
    instance_dict = {instance.name : instance for instance in instances}
    try:
        instance = instance_dict[args.instance]
    except KeyError:
        print ("no such instance", args.instance, file=sys.stderr)
        sys.exit(1)

    bounds = args.bounds
    if bounds:
        bounds = tuple(map(int, bounds.split("-")))
    else:
        bounds = (0, 2**16-1)
    print ("using instance", instance.name, instance.description, "with bounds", bounds, file=sys.stderr)
    print (mzn_instance(instance, scale=lambda t: [floor(t / args.scale), ceil(t / args.scale)][int(args.upper)], bounds=bounds))


def schedule_from_lines(lines):
    """allocate operations to machines and parse input"""

    schedule = defaultdict(list)
    for job, line in enumerate(lines):
        for op, op_string in enumerate(line):
            start, end, machine = map(int, op_string.split(","))
            op_ex = Operation(job_id=job, op_id=op, start=start, end=end, machine=machine)
            schedule[machine].append(op_ex)

    return [schedule[k] for k in sorted(schedule.keys())]

def lines_from_schedule(schedule):
    lines = []
    jobs = max([max(map(lambda op: op.job_id, m)) for m in schedule]) + 1
    ops = max([max(map(lambda op: op.op_id, m)) for m in schedule]) + 1

    print("schedule size:", jobs, ops)
    for machine in schedule:
        lines.append([f"{op.start},{op.end},{op.machine}" for op in machine])
    return lines
