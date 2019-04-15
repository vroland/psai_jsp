"""
Data structures and loading procedure for job-shop scheduling problems.
"""

import re
import sys
from collections import namedtuple

Instance = namedtuple("Instance", ["name", "description", "jobs", "num_machines"])
Job = namedtuple("Job", ["id", "operations"])
Operation = namedtuple("Operation", ["machine", "time"])

def load_instances(path):
    """
    Load all problem instances found in a file.

    Returns:
        List of scheduling problem `Instances`.
    """

    with open(path, "r") as f:
        content = f.read()

    instance_start = re.compile(r"^\s+instance\s+([\w]*)\s*$", re.MULTILINE)
    instance_block = re.compile(r"^\s[\+]{5,}(.*?)^\s[\+]{5,}", re.MULTILINE | re.DOTALL)

    instances = []

    for match in instance_start.finditer(content):
        instance_name = match.group(1).strip()
        interstr = instance_block.search(content, pos=match.end())
        lines = [s.strip() for s in interstr.group(1).strip().split("\n")]
        description, spec, *lines = lines
        num_jobs, machines = map(int, spec.split())

        def parse_job(string):
            nums = string.split()

            result = []
            for i in range(0, len(nums), 2):
                machine, time = int(nums[i]), int(nums[i+1])
                result.append(Operation(machine, time))
            return result

        jobs = [Job(id=i, operations=parse_job(l)) for i, l in enumerate(lines)]

        if len(jobs) != num_jobs:
            print ("ERROR: {} jobs declared, but only {} jobs found in {}!"
                    .format(num_jobs, len(jobs), instance_name))
            sys.exit(1)

        instances.append(Instance(
                name=instance_name,
                description=description,
                jobs=jobs,
                num_machines=machines))
    return instances

if __name__ == "__main__":
    instances = load_instances("jobshop1.txt")
    print ("loaded", len(instances), "instances.")

