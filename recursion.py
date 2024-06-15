"""
Small example to demonstrate use of functional call stack for recursion
"""

def choose (n, k):
    """
    Return C(n,k) or the number of ways to choose k elements from a set of n elements.
    Formula is n!/((n-k)! * k!)
    """
    
    def fact(i):
        if i < 1:
            return 1
        
        return i * fact(i-1)
    
    return fact(n)//(fact(n-k) * fact(k))

if __name__ == '__main__':
    n = 10
    k = 3
    print('there are',choose(n,k),f'ways to choose {k} values from a set of {n}.')
