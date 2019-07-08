# path to the minizinc executable
MINIZINC := ../psai_exercise/csp/minizinc/bin/minizinc

# Constructs flags from bounds passed by environment variables.
NAME_UPPER := $(if $(CSP_UPPER),upper,lower)
NAME_BOUNDS := $(if $(CSP_BOUNDS),$(CSP_BOUNDS),none)
USE_UPPER := $(if $(CSP_UPPER),--upper,)
USE_SCALE := $(if $(CSP_SCALE),--scale=$(CSP_SCALE),)
USE_BOUNDS := $(if $(CSP_BOUNDS),--bounds=$(CSP_BOUNDS),)

# solve the instance called $*
solve_%: work/instance_%_$(NAME_UPPER)_$(NAME_BOUNDS).mzn phony_explicit
	$(MINIZINC) src/encoding.mzn $< --statistics --output-time --all-solutions

# solve and visualize the instance called $*
vis_%: phony_explicit
	$(MAKE) solve_$* | python3 src/vis.py 2>/dev/null

# solve and visualize the instance called $* by iterative scaling
iterate_vis_%: phony_explicit
	python3 src/iterate.py $* | python3 src/vis.py 2>/dev/null



# create an instance file
work/instance_%_$(NAME_UPPER)_$(NAME_BOUNDS).mzn: data/jobshop1.txt phony_explicit
	mkdir -p work
	python3 src/mzn_instance.py $< $* $(USE_SCALE) $(USE_UPPER) $(USE_BOUNDS) > $@

# download the instance file
# Thanks to Christian Lewe for providing the converted Taillard 100x20 instance!
data/jobshop1.txt:
	mkdir -p data
	curl http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/jobshop1.txt > $@
	echo "" >> $@
	curl https://lewelup.me/public/tai_100_20.merged >> $@
	echo "++++++++++++++" >> $@

# A phony prerequisite to avoid to type every whole target name.
.PHONY: phony_explicit
phony_explicit: 

.PRECIOUS: work/instance_%_$(NAME_UPPER)_$(NAME_BOUNDS).mzn
