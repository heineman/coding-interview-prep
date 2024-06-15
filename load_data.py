"""

Given a 'data.csv' file formatted as follows:
    
    Quentin,T1,24
    Peter,T3,18
    Whitney,T8,13
    Brian,T6,43
    ...

This data could be stored in any number of ways. I've provided three. Consider which one(s) can be used for the 
widest general usage.

    load_as_worker_dictionary(file_name):
        {'Alice' : [('T9', 24), ('T3', 24), ('T9', 18)], ... }
        
    load_as_task_list(file_name):
        [None, [('Eve', 22)], None, [('Bob', 35), ('Alice', 24)] , ... ]
   
    load_as_tuple_list(file_name):
        [('Alice', 'T9', 24), ('Bob', 'T3', 35), ... ]



"""

def load_as_tuple_list(file_name):
    tuples = []                               
    with open(file_name) as file:
        for line in file:
            worker,task,time = line[:-1].split(',')
            
            entry = (worker, task, int(time))
            tuples.append(entry)
    return tuples

def load_as_task_list(file_name):
    tasks = [None]                                     # Never a T0
    with open(file_name) as file:
        for line in file:
            worker,task,time = line[:-1].split(',')
            tid = int(task[1:])                        # Extract out index position
            
            if len(tasks) <= tid:
                tasks.extend([None] * (tid - len(tasks) + 1))    # Make room
            
            entry = (worker, int(time))
            if tasks[tid]:
                tasks[tid].append(entry)
            else:
                tasks[tid] = [entry]
    return tasks
        
def load_as_worker_dictionary(file_name):
    workers = {}
    with open(file_name) as file:
        for line in file:
            worker,task,time = line[:-1].split(',')
            entry = (task, int(time))
            if worker in workers:
                workers[worker].append(entry)
            else:
                workers[worker] = [entry]
        
    return workers

if __name__ == '__main__':
    tasks = load_as_tuple_list('data.csv')
    for t in tasks:
        print(t)
        