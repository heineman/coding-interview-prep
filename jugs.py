"""
Full solution to the Jugs Logic Puzzle.
"""

from collections import deque

class State:
    def __init__(self, jug4 = 0, jug7 = 0):
        self.jug4 = jug4
        self.jug7 = jug7
        self.prev = None
        
    def __str__(self):
        return f'{self.jug4},{self.jug7}'
    
    def __eq__(self, other):
        """Equality based solely on values in jug4 and jug7 attributes."""
        return (self.jug4, self.jug7) == (other.jug4, other.jug7)
        
    def __hash__(self):
        """Provide hash so State can be properly used in a set."""
        return hash((self.jug4, self.jug7))
        
    def steps(self):
        """Possible states that result."""
        
        # Fill either one completely from external source
        if self.jug4 < 4:
            yield State(4, self.jug7)
        if self.jug7 < 7:
            yield State(self.jug4, 7)

        # empty either one
        if self.jug4 > 0:
            yield State(0, self.jug7)
        if self.jug7 > 0:
            yield State(self.jug4, 0)
            
        # how much you could add to jug4? This covers (a) emptying jug7 entirely; or (b) just partially
        diff = min(4 - self.jug4, self.jug7)
        if diff > 0:
            yield State(self.jug4 + diff, self.jug7 - diff)
            
        # how much you could add to jug7? This covers (a) emptying jug4 entirely; or (b) just partially
        diff = min(7 - self.jug7, self.jug4)
        if diff > 0:
            yield State(self.jug4 - diff, self.jug7 + diff)
        
    def is_solved(self, target):
        """Determine if jug4 or jug7 has target gallons."""
        return self.jug4 == target or self.jug7 == target
        
def search(target):
    """Search using queue."""
    q = deque()                     # Stores states to explore
    st = State()                    # Initial [0,0] state
    q.append(st)
    seen = set()                    # Set of states already seen
    while q:
        st = q.popleft()            # Retrieve state that has been in the queue the longest 
        if st in seen:              # Can ignore if already seen
            continue
        seen.add(st)                # Record that has been explored
                    
        if st.is_solved(target):
            return st
        
        for ns in st.steps():       # Compute neighboring states
            ns.prev = st            # Remember where it came from
            q.append(ns)            # Enqueue to explore in due time
    return None                     # If we get here, no solution found

def complete_search():
    """Search using queue and find fewest # of edges to find volumes (either j4 or j7) for 1 through 7."""
    q = deque()
    st = State()
    q.append(st)
    seen = set()
    volumes = [None] * 8
    while q:
        st = q.popleft()
        if st in seen:
            continue
        seen.add(st)
                    
        # Search exhaustively and take each opportunity to record first one there
        for v in range(1, 8):
            if volumes[v] is None and st.jug4 == v:
                volumes[v] = st
            if volumes[v] is None and st.jug7 == v:
                volumes[v] = st
        
        for ns in st.steps():
            ns.prev = st
            q.append(ns)
    
    for v in range(1,8):
        ct = 0
        st = volumes[v]
        while st.prev:
            st = st.prev
            ct += 1
        print (v, "in", ct, "transitions:", volumes[v])
    
def complete_search_total():
    """Search using queue and find fewest # of edges to find volumes (either j4 or j7) for 1 through 7."""
    q = deque()
    st = State()
    q.append(st)
    seen = set()
    volumes = [None] * 12
    impossible_states = [[0 for i in range(8)] for j in range(5)]
    while q:
        st = q.popleft()
        if st in seen:
            continue
        seen.add(st)
        impossible_states[st.jug4][st.jug7] = 1
                    
        # Search exhaustively and take each opportunity to record first one there
        for v in range(1, 12):
            if volumes[v] is None and st.jug4 + st.jug7 == v:
                volumes[v] = st
        
        for ns in st.steps():
            ns.prev = st
            q.append(ns)
    
    for v in range(1,12):
        ct = 0
        st = volumes[v]
        while st.prev:
            st = st.prev
            ct += 1
        print (v, "in", ct, "transitions:", volumes[v])
    
    
    print("---")
    print("Unreachable states:")
    ct = 0
    for i in range(0,5):
        for j in range(0,8):
            if impossible_states[i][j] == 0:
                print(f'Unable to get[{i}][{j}]')
                ct += 1
    print(ct,"unreachable states.")

if __name__ == '__main__':
    st = search(6)
    stack = deque()
    while st:
        stack.append(st)
        st = st.prev
    
    print("Order of States to solution")
    while stack:
        print(stack.pop())
        
    print("---")
    print("How many steps to have any jug with N gallons")
    complete_search()
    
    print("---")
    print("How many steps to have both jugs combine to hold N gallons")
    complete_search_total()
    # Can you confirm there are ways of getting 1, 2, 3, 5 gallons as well 
        
        