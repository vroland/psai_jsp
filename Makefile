MINIZINC := ../psai_exercise/csp/minizinc/bin/minizinc

NAME_UPPER := $(if $(CSP_UPPER),upper,lower)
NAME_BOUNDS := $(if $(CSP_BOUNDS),$(CSP_BOUNDS),none)

USE_UPPER := $(if $(CSP_UPPER),--upper,)
USE_SCALE := $(if $(CSP_SCALE),--scale=$(CSP_SCALE),)
USE_BOUNDS := $(if $(CSP_BOUNDS),--bounds=$(CSP_BOUNDS),)

.PHONY: phony_explicit

phony_explicit: 

work/instance_%_$(NAME_UPPER)_$(NAME_BOUNDS).mzn: data/jobshop1.txt phony_explicit
	python3 src/mzn_instance.py $< $* $(USE_SCALE) $(USE_UPPER) $(USE_BOUNDS) > $@

solve_%: work/instance_%_$(NAME_UPPER)_$(NAME_BOUNDS).mzn phony_explicit
	$(MINIZINC) src/encoding.mzn $< --statistics --output-time --all-solutions

vis_%: phony_explicit
	$(MAKE) solve_$* | src/vis.py 2>/dev/null

iterate_vis_%: phony_explicit
	python3 src/iterate.py $* | src/vis.py 2>/dev/null

.PRECIOUS: work/instance_%_$(NAME_UPPER)_$(NAME_BOUNDS).mzn
