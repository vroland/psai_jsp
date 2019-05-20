"""
Transform JSP instances to ASP instances.
"""
from parser import load_instances
from functools import reduce
import operator

def asp_encode(instance):
    """
    Arguments:
        instance: The JSP instance.
    Returns:
        String of asp facts.
    """

    def fact(name, *args):
        return "{}({}).".format(name, ",".join([str(arg).lower() for arg in args]))

    facts = []
    # instance size
    facts += [fact("job", "0.." + str(len(instance.jobs) - 1))]
    facts += [fact("machine", "0.." + str(instance.num_machines - 1))]

    # number of jobs per machine
    for machine in range(instance.num_machines):
        opcount = 0
        for job in instance.jobs:
            opcount += len(list(filter(lambda op: op.machine == machine, job.operations)))

        facts += [fact("machine_slot", machine, "0.." + str(opcount - 1))]

    # jobs and ops
    for job in instance.jobs:
        for op_id, op in enumerate(job.operations):
            facts += [fact("operation", (job.id, op_id), op.machine, op.time)]

            # mark last operation
            if op_id == len(job.operations) - 1:
                facts += [fact("last_operation", (job.id, op_id))]

    return "\n".join(facts)

if __name__ == "__main__":
    instances = load_instances("jobshop1.txt")
    print (asp_encode(instances[0]))

