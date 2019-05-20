from clingo import SymbolType
from collections import defaultdict


def dict_from_model(model):
        def unpack(s):
            if s.type == SymbolType.Number:
                return s.number
            elif s.type == SymbolType.String:
                return s.string
            elif s.type == SymbolType.Function:
                return tuple(map(unpack, s.arguments))

        terms = model.symbols(atoms=True)
        follows = defaultdict(set)

        for term in terms:
            if term.name == "directly_follows":
                op1, op2 = unpack(term)
                follows[op1].add(op2)

        return follows

def vis_model(model):
    follows = dict_from_model(model)
    start = []
    for k in follows.keys():
        for v in follows.values():
            if k in v:
                break
        else:
            start.append(k)
    print (start)
    print (follows)
