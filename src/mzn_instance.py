"""
Transform JSP instances to minizinc format.
"""

import sys
from parser import load_instances

def mzn_instance(instance):

    def range(name, to):
        return [
            "int: num_{} = {}".format(name, to),
            "set of int: {} = 1..num_{}".format(name.upper(), name)
        ]

    # ranges
    facts = range("jobs", len(instance.jobs))
    facts += range("machines", instance.num_machines)
    facts += range("operations", len(instance.jobs[0].operations))

    oplengths = []
    opmachines = []
    for job in instance.jobs:
        oplengths += ["{}|".format(", ".join([str(op.time) for op in job.operations]))]
        opmachines += ["{}|".format(", ".join([str(op.machine) for op in job.operations]))]

    facts += ["array[JOBS, OPERATIONS] of int: oplengths = [|\n{}]".format("\n".join(oplengths))]
    facts += ["array[JOBS, OPERATIONS] of int: opmachines = [|\n{}]".format("\n".join(opmachines))]
    return ";\n".join(facts)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='generate a minizinc instance')
    parser.add_argument('infile', help='a file to search for instances')
    parser.add_argument('instance', help='name of the instance to use')

    args = parser.parse_args()
    instances = load_instances(args.infile)
    instance_dict = {instance.name : instance for instance in instances}
    try:
        instance = instance_dict[args.instance]
    except KeyError:
        print ("no such instance", args.instance, file=sys.stderr)
        sys.exit(1)

    print ("using instance", instance.name, instance.description, file=sys.stderr)
    print (mzn_instance(instance))



