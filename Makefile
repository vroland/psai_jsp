MINIZINC := ../psai_exercise/csp/minizinc/bin/minizinc

work/instance_%.mzn: data/jobshop1.txt
	python3 src/mzn_instance.py $< $* > $@

.PHONY: solve_%
solve_%: work/instance_%.mzn
	$(MINIZINC) src/encoding.mzn $< --statistics --all-solutions

.PHONY: vis_%
vis_%:
	$(MAKE) solve_$* | src/vis.py

