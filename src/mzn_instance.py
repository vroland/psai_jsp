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
    instances = load_instances("jobshop1.txt")
    instance = instances[-6]
    print ("using instance", instance.name, instance.description, file=sys.stderr)
    print (mzn_instance(instance))



