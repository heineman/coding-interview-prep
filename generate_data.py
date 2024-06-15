"""
Generate Random data set for worker problem. Then show different ways to load information from a comma-separated file.

  1. Each name is equally likely to be selected from the 'names' list.
  2. Tasks are numbered from T1 to T40, and tasks T1-T9 are more likely to be selected than tasks T10-T40.
  3. Times in minutes are selected following Gaussian distribution with mean of 30 and sigma of 8. Won't be smaller than 10.
  
Placed in 'data.csv' file

From this CSV file, the input.py file contains three different methods to load up the data into different structures.

"""

names = ['Alice', 'Bob', 'Connor', 'Daniel', 'Eve', 'Francis', 'Grace', 'Harry', 'Isabella', 'Jacob', 'Kerry', 'Luke', 
'Molly', 'Nicholas', 'Olivia', 'Peter', 'Quentin', 'Rachel', 'Sydney', 'Taylor', 'Uma', 'Victor', 'Whitney','Xena', 'Yvonne', 'Zachary']

output = 'data.csv'

trials = 500
    
import random

if __name__ == '__main__':
    file = open(output, "w")
    for _ in range(trials):
        name = random.choice(names)
        
        # More frequently (60% of the time) choose from T1 - T9
        if random.random() > .4:
            tid = random.randint(1,9)
        else:
            tid = random.randint(10,40)
        
        # Make sure at least 10 minutes
        length = max(10, int(random.gauss(30,8)))
        
        # Proper format
        file.write(f'{name},T{tid},{length}\n')
    file.close()
    