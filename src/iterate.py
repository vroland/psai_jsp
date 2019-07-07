import subprocess
import threading
import re
import math
import sys
from mzn_instance import schedule_from_lines, lines_from_schedule

SCALES = [64, 32, 16, 8, 4, 2, 1]

TIMEOUT = 60

def get_bound(scale, upper, bounds, instance):
    env = {
        "CSP_SCALE": str(scale),
        "CSP_UPPER": "TRUE" if upper else "",
        "CSP_BOUNDS": f"{bounds[0]}-{bounds[1]}"
    }

    result = subprocess.run(["make", f"solve_{instance}"], stdout=subprocess.PIPE, env=env, timeout=TIMEOUT)
    out = result.stdout.decode("utf-8")
    lengths = re.findall("^l:([0-9]+)$", out, flags=re.MULTILINE)
    instance = re.search("^([^-]*)l:"+lengths[-1]+"$[^-]*[-]{3,}$", out, flags=re.MULTILINE);
    lines = [l.strip()[2:].split() for l in instance.group(1).split("\n") if l.strip()]
    schedule = schedule_from_lines(lines)

    #for machine in schedule:
    #    for op in machine:
    #        op.start *= scale
    #        op.end *= scale

    return (schedule, int(lengths[-1]) * scale)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='solve a JSP instance by bounds scaling')
    parser.add_argument('instance', help='name of the instance to use')
    args = parser.parse_args()

    lower = 0
    upper = 2**16-1
    upper_schedule = None

    for scale in SCALES:
        print ("current scale is:", scale, file=sys.stderr)
        bounds = (lower, upper)
        def calc_lb():
            global lower
            (_, lower) = get_bound(scale, False, bounds, args.instance)
        def calc_ub():
            global upper, upper_schedule
            (upper_schedule, upper) = get_bound(scale, True, bounds, args.instance)

        t1 = threading.Thread(target=calc_lb);
        t2 = threading.Thread(target=calc_ub);
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print(f"new bounds: {lower}..{upper}", file=sys.stderr)
        schedule_text = "\n".join(["m:"+" ".join(l) for l in lines_from_schedule(upper_schedule)])
        print("new plan:")
        print(schedule_text)
        print("-----------")
        sys.stdout.flush()
