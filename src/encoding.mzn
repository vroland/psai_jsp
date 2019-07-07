array[JOBS, OPERATIONS] of var int: starts_at;
var int: end;

% all start times are greater than zero
constraint forall(j in JOBS)(forall(o in OPERATIONS)(starts_at[j, o] >= 0));

% operations of the same job are ordered (closure performs better than only direct succesor)
constraint forall(j in JOBS)(
	forall(o1, o2 in OPERATIONS where o1 < o2)(
		starts_at[j, o2] >= starts_at[j, o1] + oplengths[j, o1]
	)
);

% one machine can only run one operation at a time
constraint forall(j1, j2 in JOBS, o1, o2 in OPERATIONS)(
    opmachines[j1, o1] == opmachines[j2, o2] /\ (j1 != j2 \/ o1 != o2) -> 
        starts_at[j1, o1] + oplengths[j1, o1] <= starts_at[j2, o2] \/ 
        starts_at[j2, o2] + oplengths[j2, o2] <= starts_at[j1, o1]
);

% lower bound of operations
constraint forall(j in JOBS)(
    forall(o in OPERATIONS where o < num_operations)(
        starts_at[j,o] >= sum(o2 in OPERATIONS where o2 < o)(oplengths[j, o2])
    )
);

constraint forall(j in JOBS)(
    forall(o in OPERATIONS)(
        starts_at[j,o] <= UPPER_BOUND - sum(o2 in OPERATIONS where o2 >= o)(oplengths[j, o2])
    )
);

% one operation must be directly followed by another
%constraint forall(j in JOBS)(
%    forall(o in OPERATIONS where o < num_operations)(
%        exists(j2 in JOBS, o2 in OPERATIONS)(starts_at[j2,o2] = starts_at[j, o] + oplengths[j, o] /\ (j != j2 \/ o != o2))
%    )
%);

constraint end = max(j in JOBS)(starts_at[j, num_operations] + oplengths[j, num_operations]);


constraint UPPER_BOUND >= end;
constraint end >= LOWER_BOUND;

solve minimize end;

output [ 
    if o == 1 then "\nm:" else " " endif ++ 
        show(starts_at[j, o]) ++ "," ++ 
        show(starts_at[j, o] + oplengths[j, o]) ++ "," ++ 
        show(opmachines[j, o]) 
| j in JOBS, o in OPERATIONS ] ++ ["\nl:" ++ show(end)];
