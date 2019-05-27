array[JOBS, OPERATIONS] of var int: starts_at;

% all start times are greater than zero
constraint forall(j in JOBS)(forall(o in OPERATIONS)(starts_at[j, o] >= 0));

% operations of the same job are ordered
constraint forall(j in JOBS)(
	forall(o in OPERATIONS)(
		if o > 1 then starts_at[j, o] >= starts_at[j, o-1] + oplengths[j, o-1] endif
	)
);

% one machine can only run one operation at a time
constraint forall(j1, j2 in JOBS, o1, o2 in OPERATIONS)(
    opmachines[j1, o1] == opmachines[j2, o2] /\ (j1 != j2 \/ o1 != o2) -> 
        starts_at[j1, o1] + oplengths[j1, o1] <= starts_at[j2, o2] \/ 
        starts_at[j2, o2] + oplengths[j2, o2] <= starts_at[j1, o1]
);

%solve satisfy;
solve %:: int_search(starts_at, first_fail, indomain_min, complete)
minimize max(j in JOBS)(starts_at[j, num_operations] + oplengths[j, num_operations]);

output [ 
    if o == 1 then "\nm:" else " " endif ++ 
        show(starts_at[j, o]) ++ "," ++ 
        show(starts_at[j, o] + oplengths[j, o]) ++ "," ++ 
        show(opmachines[j, o]) 
| j in JOBS, o in OPERATIONS ];
