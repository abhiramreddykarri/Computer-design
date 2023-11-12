def f(g, s, fst):
    if s not in g:
        return {s}
    if s in fst:
        return fst[s]
    fs = set()
    for p in g[s]:
        if p == 'eps':
            fs.add('eps')
        else:
            for sym in p:
                pfs = f(g, sym, fst)
                fs |= (pfs - {'eps'})
                if 'eps' not in pfs:
                    break
            else: fs.add('eps')
    fst[s] = fs
    return fs

def fl(g, s, st, flw, fst):
    if s == st:
        flw[s].add('$')
    for lhs, ps in g.items():
        for p in ps:
            if s in p:
                idx = p.index(s)
                nxt = p[idx + 1:]
                if nxt:
                    nfs = set()
                    for ns in nxt:
                        nfs |= f(g, ns, fst)
                        if 'eps' not in nfs:
                            break
                    flw[s] |= (nfs - {'eps'})
                if not nxt or 'eps' in nfs:
                    if lhs != s:
                        flw[s] |= fl(g, lhs, st, flw, fst)
    return flw[s]

def comp_ff(g):
    fst = {nt: set() for nt in g}
    flw = {nt: set() for nt in g}
    for nt in g:
        f(g, nt, fst)
    st = next(iter(g))
    fl(g, st, st, flw, fst)
    return fst, flw

g = {
    'E': ['TG'],
    'G': ['+TG', 'eps'],
    'T': ['FH'],
    'H': ['*FH', 'eps'],
    'F': ['(E)', 'i']
}
fst, flw = comp_ff(g)

print("FIRST sets:")
for nt, fs in fst.items():
    print(f"{nt}: {fs}")
print("\nFOLLOW sets:")
for nt, fw in flw.items():
    print(f"{nt}: {fw}")
