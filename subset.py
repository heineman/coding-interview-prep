"""
A collection of different solutions for the Subset Sum problem.

1. subset_sum_exists() uses memoization to return True or False if a subset exists whose sum is target.
2. subset_sum() uses memoization and returns a subset whose sum equals the target.
3. subset_sum_results() uses a different strategy for recovering the solution that is easier to explain.
"""

import itertools

def brute_force(A, target):
    # Each possible subset of given size
    for n in range(1,len(A)+1):
        for sub in itertools.combinations(A, n):
            if sum(sub) == target:
                return sub
    return None

def subset_sum_exists(A, target):
    results={}
    def recursive(hi, partial):
        """Is there a subset of A matching partial?"""
        if partial == 0: return True
        if hi < 0: return False

        # adding last one would be too much
        if A[hi] > partial: 
            val = recursive(hi-1, partial)
        else:
            # second case has two sub-cases
            with_last = recursive(hi-1, partial - A[hi])
            without   = recursive(hi-1, partial)
            val       = with_last or without
            
            results[(hi, partial)] = val 
        return val
    
    return recursive(len(A)-1, target)

def subset_sum(A, target):
    results={}
    def recursive(hi, partial):
        """Is there a subset of A matching partial?"""
        if partial == 0: return True
        if hi < 0: return False
        if (hi, partial) in results: return results[(hi, partial)]

        # adding last one would be too much
        if A[hi] >= partial: 
            val = recursive(hi-1, partial)
        else:
            # second case has two sub-cases
            with_last = recursive(hi-1, partial - A[hi])
            without   = recursive(hi-1, partial)
            val       = with_last or without
            
            results[(hi, partial)] = val 
        return val

    def solved(last, part):
        return (last,part) in results and results[(last, part)]

    answer = []
    if recursive(len(A)-1, target):
        hi, partial = len(A)-1, target
        while hi >= 0 and partial > 0:
            newtarget = partial-A[hi]
            if A[hi] == partial or solved(hi-1, newtarget):
                answer.append(A[hi])    # Keep A[hi]
                partial = newtarget
            hi -= 1
    return answer

def subset_sum_result(A, target):
    results = {}
    def recursive(hi, partial):
        """Is there a subset of A matching partial?"""
        if partial == 0: return True
        if hi < 0: return False
        if (hi, partial) in results: return results[(hi, partial)]
        
        result = recursive(hi-1, partial)
        if A[hi] <= partial and not result: 
            result = recursive(hi-1, partial - A[hi])
            
        # Was A[hi] used in solving partial problem?
        results[(hi,partial)] = result         
        return result

    answer = []
    if recursive(len(A)-1, target):
        decisions = [0] * len(A)
        for hi,partial in results:
            if results[(hi,partial)]:
                decisions[hi] = partial
        
        last = 0
        for i in range(len(A)):
            diff = decisions[i] - last
            if diff > 0:
                answer.append(A[i])
            last = decisions[i]
    return answer

if __name__ == '__main__':
    target = 46
    A = [3, 5, 7, 11, 13, 17]
    print(f'has subset sum to {target}: {brute_force(A,target)}')
    B = [10, 9, 8, 23, 4, 12, 17, 58]
    target = 53
    print(f'has subset sum to {target}: {subset_sum_result(B,target)}')
    
    import random
    X = list(range(90))
    for _ in range(100):
        random.shuffle(X)
        s1 = subset_sum_result(X, 130)
        if sum(s1) != 130:
            print("BAD")
            