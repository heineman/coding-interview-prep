"""
Solution for Longest Common Subsequence (LCS) using recursion and tabulation.

Note the Recursion solution is actually quite inefficient because it creates string prefixes unnecessarily,
but it is easier to explain this way.

lcs_optimized provides a recursive implementation using the index values of si and ti to refer to the prefix within
si and ti. It also uses memoization to avoid redoing past problems AND it returns the actual subsequence, not just 
the length of the longest common subsequence.
"""

def lcs(s, t):
    if len(s) == 0 or len(t) == 0:
        return 0

    s_prefix = s[:-1]
    t_prefix = t[:-1]

    if s[-1] == t[-1]:
        return 1 + lcs(s_prefix, t_prefix)
    else:
        return max(lcs(s, t_prefix), lcs(s_prefix, t))

def lcs_optimized(s, t):
    results = {}
    
    def inner(si, ti):
        if si < 0 or ti < 0:
            return 0
        
        if (si,ti) in results:
            return results[(si,ti)]
    
        if s[si] == t[ti]:
            val = 1 + inner(si-1, ti-1)
        else:
            LS2a = inner(si, ti-1)
            LS2b = inner(si-1, ti)
            val = max(LS2a, LS2b)    
        
        results[(si,ti)] = val
        return val
    
    si = len(s)-1
    ti = len(t)-1
    inner(si, ti)
    lcs = ''
    while si >= 0 and ti >= 0:
        # if s[i] and t[i] are same, it is part of LCS
        if s[si] == t[ti]:
            lcs += s[si]
            si,ti = si-1,ti-1
        else:
            LS2a = 0 if ti == 0 else results[(si,ti-1)]
            LS2b = 0 if si == 0 else results[(si-1,ti)]
            if LS2a > LS2b:
                ti -= 1
            else:
                si -= 1
    results = {}
    return lcs[::-1]

def lcs_tabulate(s, t):
    sN, tN = len(s), len(t)
    LCS = [[0] * (tN+1) for _ in range(sN+1)]

    for si in range(1, sN + 1):
        for ti in range(1, tN + 1):
            if s[si-1] == t[ti-1]:
                LCS[si][ti] = 1 + LCS[si-1][ti-1]
            else:
                LCS[si][ti] = max(LCS[si-1][ti], LCS[si][ti-1])

    print (LCS)
    return LCS[sN][tN]

if __name__ == '__main__':
    print(lcs('state', 'stealth'))
    print(lcs_tabulate('state', 'stealth'))
    
    print(lcs_tabulate('heart', 'hat'))
    print(lcs_optimized('REWARD' , 'DRAWER'))
    print(lcs_optimized('TEAM' , 'META'))
