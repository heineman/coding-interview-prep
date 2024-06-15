"""
Dp vs. Divide-and-Conquer

Recursion vs. Iterative
"""
import random

def largest_value(A):
    """Find largest value in a list using a for loop."""
    if len(A) == 0:
        raise ValueError('largest() arg is an empty sequence')
    
    m = A[0]
    
    for i in range(1,len(A)):
        if A[i] > m:
            m = A[i]
    return m

def largest_value_rec(A):
    """Find largest value in a list using recursion"""      
    def large(lo, hi):
        if lo == hi:           # Base Case: just one element, A[lo]
            return A[lo]
        
        mid = (lo + hi) // 2
         
        L = large(0, mid)
        R = large(mid+1, hi)
         
        return max(L, R)
    
    if len(A) == 0:
        raise ValueError('largest() arg is an empty sequence')
    
    return large(0, len(A)-1)

def largest_sublist(A):
    """Find largest increasing sublist in a list using a for loop."""
    best_idx, best_size = 0, 1
    idx, size = 1, 1

    while idx < len(A):
        if A[idx-1] < A[idx]:     # Still increasing
            size += 1
            if size > best_size:  # New record?
                best_idx, best_size = idx - size + 1, size
        else:
            size = 1
        idx += 1
        
    return A[best_idx:best_idx + best_size]

def largest_sublist_rec(A):
    """Find largest increasing sublist in a list using Recursion."""
        
    def large(lo, hi):
        """Returns Tuple (a) Starting position of longest run; (b) its length; (c) length of run that starts at lo; (d) length of run that ends at hi."""
        
        if lo == hi:
            return (lo, 1, 1, 1)
        
        mid = (lo + hi) // 2
        
        L_start, L_len, L_lo, L_hi = large(lo, mid)          # Divide into two
        R_start, R_len, R_lo, R_hi = large(mid+1, hi)
        
        # Either:
        # (a) L has the longest run; or
        # (b) R has the longest run; or
        # (c) longest run starts in L and continues into R
        
        # Chance to extend from left side into right side...
        if L_hi + R_lo > L_len and L_hi + R_lo > R_len and A[mid] < A[mid+1]:
            new_lo = L_lo
            
            new_hi = R_hi

            # Chance to extend Left sublist into Right sublist
            if A[mid] < A[mid+1]: 
                if lo + L_lo == mid + 1:
                    new_lo += R_lo
                
                if hi - R_lo == mid:
                    new_hi += L_hi
                                
            return (mid - L_hi + 1, L_hi + R_lo, new_lo, new_hi)

        if L_len > R_len:
            return (L_start, L_len, L_lo, R_hi)
        else:
            return (R_start, R_len, L_lo, R_hi)
    
    if len(A) == 0:
        return []
    start, length, _, _ = large(0, len(A)-1)
    return A[start:start+length]    

def lis_rec(A):
    """Given List of values, find longest increasing subsequence (NOT sublist)"""
    
    def lis(hi):
        if hi == 0:              # Base Case
            return 1
        
        longest = 1
        for j in range(hi):
            if A[j] < A[hi]:
                longest = max(longest, 1 + lis(j))
        return longest
    
    result = 1
    for i in range(len(A)):
        result = max(result, lis(i))
    return result

def lis_rec_memo(A):
    """Given List of values, find longest increasing subsequence (NOT sublist)"""
    
    memo = {}
    
    def lis(hi):
        if hi == 0:              # Base Case
            return 1
        
        if hi in memo: return memo[hi]
        
        longest = 1
        for j in range(hi):
            if A[j] < A[hi]:
                longest = max(longest, 1 + lis(j))
        memo[hi] = longest
        return longest
    
    result = 1
    for i in range(len(A)):
        result = max(result, lis(i))
    return result

def shuffled(A):
    random.shuffle(A)
    return A

def lis(A):
    """Given List of values, find longest increasing subsequence (NOT sublist) using tabulation."""
    N    = len(A)
    LIS  = [1] * N      # Length of longest subsequence ENDING at A[j]
    
    for i in range(N):
        for j in range(i):
            # If an existing longest subsequence ends at J with length LIS[j], 
            # and A[i] (to the right of A[j]) is actually bigger than A[j], then
            # you might have a new longest subsequence ending at A[i] if LIS[j]+1 > LIS[i] 
            if A[j] < A[i] and LIS[j] + 1 > LIS[i]:
                LIS[i] = LIS[j] + 1
                
    return max(LIS)

def lis_with_solution(A):
    """Tabular approach for LIS that also computes sequence itself."""
    N    = len(A)
    LIS  = [1] * N      # Length of longest subsequence ENDING at A[j]
    prev = [-1] * N 
    
    for i in range(N):
        for j in range(i):
            # If an existing longest subsequence ends at J with length LIS[j], 
            # and A[i] (to the right of A[j]) is actually bigger than A[j], then
            # you might have a new longest subsequence ending at A[i] if LIS[j]+1 > LIS[i] 
            if A[j] < A[i] and LIS[j] + 1 > LIS[i]:
                LIS[i] = LIS[j] + 1
                prev[i] = j
                
    m = max(LIS)
    i = LIS.index(m)
    
    result = []
    while i != -1:
        result.append(A[i])
        i = prev[i]
    result.reverse()
    return (m, result)

def timing_lis_trial():
    """Timing lis on random lists of size N."""
    import timeit
    
    for k in range(6, 12):
        N = 2 ** k
        result = timeit.timeit(f'lis(shuffled(R))', setup=f'R=list(range({N}))', globals = globals(), number=100)
        result /= 100
        print('lis', N, result)

def timing_lis_rec_trial():
    """Timing lis_rec on random lists of size N."""
    from timeit import timeit
    T = 100
    for N in range(30, 66, 5):
        result = timeit(f'lis_rec(shuffled(R))', setup=f'R=list(range({N}))', globals = globals(), number=T)
        result /= T
        print('lis_rec', N, result)

def timing_lis_rec_memo_trial():
    """Timing lis_rec_memo on random lists of size N."""
    import timeit
    
    for k in range(6, 12):
        N = 2 ** k
        result = timeit.timeit(f'lis_rec_memo(shuffled(R))', setup=f'R=list(range({N}))', globals = globals(), number=100)
        result /= 100
        print('lis_rec_memo', N, result)

#timing_lis_rec_memo_trial()
counting = {}
def fib(N):
    counting[N] = 1 if N not in counting else counting[N] + 1
        
    if N <= 0: return 0
    if N == 1: return 1
    return fib(N-1) + fib(N-2)


def fibm(N, memo = None):
    if N <= 0: return 0
    if N == 1: return 1
    if memo == None: memo = {}
    if N in memo: return memo[N]
    
    memo[N] = fibm(N-1, memo) + fibm(N-2, memo) 
    return memo[N]

if __name__ == "__main__":
    print("Compare recursive vs. nonrecursive sublist implementations")
    for _ in range(10000):
        R = list(range(random.randint(0,30)))
        random.shuffle(R)
        one = largest_sublist(R)
        two = largest_sublist_rec(R)
        if one == two:
            pass
        elif len(one) == len(two):
            pass 
        else:
            print ("Difference: ", one, "vs.", two)

    print("Compare all LIS implementations")
    for _ in range(10000):
        R = list(range(random.randint(1,30)))
        random.shuffle(R)
        R.append(0)
        len1 = lis(R)
        len2 = lis_rec(R)
        len3 = lis_rec_memo(R)
        (len4,sol4) = lis_with_solution(R)
        results = set()
        results.add(len1)
        results.add(len2)
        results.add(len3)
        results.add(len4)
        if len(results) != 1:
            print("BAD")

    print ("DONE")
