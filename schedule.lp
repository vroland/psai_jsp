

% jobs on the same machine must be ordered
1 { follows(OP1, OP2) } 1 :- operation(OP1, M, _), operation(OP2, M, _), OP1 != OP2.
% operations of the same job are ordered
%follows((J, O1), (J, O2)) :- operation((J, O1), _, _), operation((J, O2), _, _), O1 < O2.

% every not-final operation as successors
1 { directly_follows(OP, OP2) : operation(OP2, _, _) } :- operation(OP, _, _), not last_operation(OP).
% every operation has at most one predecessor
0 { directly_follows(OP1, OP2) } 1 :- operation(OP1, _, _), operation(OP2, _, _), OP1 != OP2.

% "follows" is transitive closure of "directly follows"
follows(OP1, OP2) :- directly_follows(OP1, OP2).
follows(OP1, OP3) :- follows(OP1, OP2), directly_follows(OP2, OP3).

%follows_in(OP1, OP2, T1 + T2) :- directly_follows(OP1, OP2), operation(OP1, _, T1), operation(OP2, _, T2).
%follows_in(OP1, OP3, T1 + T2) :- follows_in(OP1, OP2, T1), directly_follows(OP2, OP3), operation(OP3, _, T2).

#show. 

#script (python)
from vis import vis_model

def main(prg):
    prg.ground([("base", [])])
    with prg.solve(yield_ = True) as handle:
        model = None
        for m in handle:
            model = m
            vis_model(m)
        print ("done!")
#end.
