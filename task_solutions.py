"""
Contains different solutions for the tasks covered in Module 1. 
"""


"""
Task: Remove redundant (worker, task) entries with lower times, only keeping highest values, in the input data.
"""
def reduce_pairs(data):
    result = {}                      # Use dict (pair) -> MaxTime
    for d in data:
        key = d[:2]                  # Extract pair to use as key
        if key not in result:
            result[key] = d[2]       # First time? Record value
        else:
            if d[2] > result[key]:   # Update if greater than recorded
                result[key] = d[2]
    
    out = []                         # Convert dict back into tuple list
    for r in result.keys():
        triple = r + (result[r],)    # Create a tuple from SINGLE value
        out.append(triple)           # re-create triple
    return out

"""
Task: Find the worker(s) who can perform the most tasks in the input data.
"""
def most_tasks(data):
    most = {}                        # a dictionary
    for d in data:                   # store in dictionary (worker) -> [tasks]
        worker, task = d[:2]
        if worker in most:
            most[worker].add(task)   # Might add to set
        else:
            most[worker] = {task}    # Collect set of tasks for each worker
    
    highest = -1                     # find worker(s) with most number of tasks
    result = []
    for worker in most:              # Iterate over dictionary 
        total = len(most[worker])    #    and keep (highest, list of workers)
        if total == highest:         # equals most? Add to list
            result.append(worker)
        elif total > highest:        # greater than most? create anew
            highest, result = total, [worker]
    return (highest, result)

"""
Task: Find the least amount of total time to complete all tasks in the input data
"""
def least_time(data):
    tasks = {}
    for d in data:
        _, task, time = d
        if task in tasks:
            if time < tasks[task]:
                tasks[task] = time
        else:
            tasks[task] = time

    total = 0
    for task in tasks:
        total += tasks[task]
    return total

"""
Task: Find a worker who can complete the most tasks in the least amount of time in the input data.
"""
def best_worker(data):
    workers = {}
    for d in data:
        worker, task, time = d
        if worker not in workers:
            workers[worker] = {task:time}
        else:
            if task in workers[worker]:
                if time < workers[worker][task]:
                    workers[worker][task] = time
            else:
                workers[worker][task] = time

    mostTasks = -1
    leastTime = float('inf')
    best = None
    for worker in workers:
        numTasks = len(workers[worker])
        totalTime = sum(workers[worker].values())
        if numTasks > mostTasks:
            best,mostTasks,leastTime = worker,numTasks,totalTime
        elif numTasks == mostTasks:
            if totalTime < leastTime:
                best,leastTime = worker,totalTime

    return (best, leastTime)

"""
Helper Task: Return (worker, task, time) that is least time for all tasks.
"""
def reduce_tasks_min(data):
    result = {}                      # Use dict (task) -> MinTime
    for d in data:
        key = d[1]                   # Extract task to use as key
        if key not in result:
            result[key] = d          # First time? Record value
        else:
            if d[2] < result[key][2]:# Update if smaller than recorded
                result[key] = d
    
    return result.values()

"""
Task: Use Greedy approach to schedule tasks to minimize completion time.
"""
def schedule(data):
    vals = reduce_tasks_min(data)    # Use helper method to find min times

    def sort_by(entry):              # Sorts tasks by work time
        return entry[2]

    return sorted(vals, key=sort_by) # Return list sorted by time 

if __name__ == "__main__":
    from load_data import load_as_tuple_list
    data = load_as_tuple_list('data.csv')
    reduced = reduce_pairs(data)
    print("Reduced has:",len(reduced),"entries from original input of size", len(data))
    
    print("Most Tasks:")
    print(most_tasks(reduced))
    
    print("Least amount of time:")
    print(least_time(reduced))
    
    print("Who are the best workers:")
    print(best_worker(reduced))
    
    print("Produce schedule that minimizes completion time")
    print(schedule(data))


