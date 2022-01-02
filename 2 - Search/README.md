# ASSIGNMENT 1

### Members:
#### Himanshu Himanshu - hhimansh@iu.edu
#### Aman Chaudhary - amanchau@iu.edu
#### Varsha Ravi Varma - varavi@iu.edu	
	   	


## PART 1:

Question 1 involves a problem based on a puzzle which requires us to find a heuristic that would arrange the board in an optimal way to reach the goal state. 

### Observation:

Firstly, we analysed the skeleton code given on the github repository to check for all the mentioned functions. We noticed that all the boards used for testing are 5 x 5 and therefore the goal state will be the same for any inputted board. The ‘printable_board’ function is used to return the board used in the program, the ‘successors’ function should return all the successor states of the board, ‘is_goal’ function is defined to store and compare the current state and the goal state and ‘solve’ function is where we will need to implement the search algorithm. 

**State space:** All boards that can be reached from the initial board using the moves.

**Initial state:** Initial board (misplaced board) that is considered as the input for the given program.

**Goal state:** Final arranged board which is the expected output for the given program. In this problem, the goal state is always (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25).

**Successor state:** We will get 24 successor states which are as follows: 5 right moves, 5 left moves, 5 up moves, 5 down moves, 2 clockwise and 2 counterclockwise.

**Cost function:** 1

### Approach and design decisions:

**Abstraction technique:** A* search

**Assumption:** A solution always exists.

We implemented the heuristic cost in a newly created ‘heuristic(current state)’ function where we calculate the sum of Manhattan distances. Then we alter the ‘is_goal’ function by defining the goal state and comparing it to the current state to check if we have reached the goal state (returns true if it has reached). In ‘successor(state)’ function, we add loops that calculates the board movements leading to the successor states, i.e., movements including right (5 states), left (5 states), up (5 states), down (5 states), outer clockwise (1 state), inner clockwise (1 state), outer counterclockwise (1 state) and inner counterclockwise (1 state). It returns a list of tuples which contains the current move (eg. R3, L2, U4, D1, Ic, Occ, etc), the cost and the board that we get after the current move. In the ‘solve(initial_board)’ function, we have converted the board in tuple format to a nested list. Then we have defined a dictionary that holds the priority as the key and the value is a list of tuples associated with the key that contains the initial board, cost and path. We have defined a visited list that keeps track of all the visited states. We iterate through the fringe and in each iteration we are finding the minimum priority and extracting one of the elements associated with it. We call the other functions to extract the successor states and we are calculating the cost of the successor state and if the cost is already in the fringe, we will directly append the state into the cost otherwise we add it newly. We repeat this until the goal state is reached and the solution path is returned when the goal state has been reached.

**In this problem, what is the branching factor of the search tree?**
The branching factor of the search tree is 24 because we get 24 successor states (5 right, 5 left, 5 up, 5 down, 1 outer clockwise, 1 outer counterclockwise, 1 inner clockwise and 1 inner counterclockwise).

**If the solution can be reached in 7 moves, about how many states would we need to explore we found it if we used BFS?** 
24^7 + 24^6 + 24^5 + 24^4 + 24^3 + 24^2 + 24^1+ 24^0

### Challenges

We first used misplaced tiles as the heuristic but it wasn’t admissible and therefore we tried using basic Manhattan and  Euclidean, but all of these were not admissible as well. We then went back to using (misplaced tiles)/5 heuristic, but it wasn’t admissible either. We then implemented some heuristics like Maximum Manhattan distance which even though were admissible but were not fast enough and were caught in timeouts.

## PART 2:
Question 2 involves a problem to find a path between two cities depending upon 4 different cos factors.

### Observation

**State space:** All the cities that we may traverse while travelling from the start city to the  end city keeping in mind the cost factor.

**Initial state:** It is the start city that is given as the input.

**Goal state:** It is the end city with the minimum cost factor given as input.

**Successor state:** All the cities which can be traversed from the current city.

**Cost function:** There are 4 different cost functions depending upon the cost given as the input that is distance, segments, delivery hour and time. Cost for the segment function is always 1 and the rest depends on the highway connecting two cities. Distance depends on the length of the highway, time depends upon the length and the speed limit and delivery hours also depends on the length, speed limit and aslo on distance traveled form start city to start point of the highway.

### Approach and design decisions

**Abstraction technique:** A* search

**Assumption:** There is always a path between 2 cities.

In the already given ‘get_route” function, firstly we read the two dataset files given and stored the data  given in it into python data structure. Depending upon  the inputted cost, we call different functions to get the desired route by minimising the minimum cost. If the cost desired is ‘distance’, we use ‘get_route_dist’ function in which we take the heuristic cost as euclidean distance.  If the cost desired is ‘segment’, we use ‘get_route_segment’ in which we set 1 as the heuristic cost. If the cost desired is ‘time’, we use ‘get_route_time’ function in which we take the heuristic cost as euclidean distance divided by average speed (average speed = sum of speed on all the highways/number of highways). If the cost desired is ‘delivery’, we use ‘get_route_del’ function in which we take the heuristic cost the same as that for ’time’. In each of the previously mentioned functions,  we have defined a dictionary that holds the priority as the key and the value is a list of tuples associated with the key that contains the start city, number of segments traveled, distance traveled, time taken, delivery hours and the route taken. We have defined a visited list that keeps track of all the visited states. We iterate through the fringe and in each iteration we are finding the minimum priority and extracting one of the elements associated with it. We call the other functions to extract the successor states and we are calculating the cost of the successor state and if the cost is already in the fringe, we will directly append the state into the cost otherwise we add it newly. We repeat this until the goal state is reached and we return a dictionary containing total segments, total miles, total hours, total delivery hours and the route taken.

### Challenges

The main challenge faced by us was to find the delivery hour between two cities by the formula given in assignment problem. We used the Q&A community to understand the formula to calculate the delivery hour. 


## PART 3:

Question 3 involves a problem to find groups of students with minimised cost.

### Observation

**State space:** All the states that can be generated upon shifting the conflicting members and the initial state with the minimum number of groups and every student is present in one of the groups.

**Initial state:** Initial state with the minimum number of groups and every student is present in one of the groups.

**Goal state:** No predefined goal state, goal is to minimize the overall cost of assigned groups.

**Successor state:** Assign the most conflicting student in different permutations to minimize cost. 

**Cost function:** Cost of most conflicting student.

### Approach and design decisions

**Abstraction technique:** Local search

To begin with, we have created a method to read the input file. We have initialized a preferences dictionary for storing preferences of each student. We have also initialized a student’s list to store all the students. Moving forward, we have read the file containing all the student data by traversing through each line of the file. We have split each line by spaces to get all the answers entered by a student. We have retrieved the wanted team members by splitting it by ‘- ’ and getting the list of rest of the members. Then, we have calculated the number of team members that are required by the student. Now, we have checked if ‘zzz’ or ‘xxx’ is present in the wanted members list, if it is present, we have removed it. Now, we have retrieved the not wanted team members by splitting it with ‘,’ and then we have checked if ‘_’ is present in the not wanted members list, if it is not present, we have removed it. Now, we have added the student details to the dictionary and appended the student’s name to the students list. We have returned a tuple of preferences and students. Then we have found the most conflicting student i.e., the student with the most conflicting cost. For this we have iterated on every row and checked if the student is in that row finding the column in particular row and returning row and column as a tuple. Moving ahead we have calculated the cost of the assigned groups and the conflicting cost of each student. Then we have initialized a dictionary of conflicting cost with student name.  We have also initialised cost variable with number of groups multiplied by 5. Moving ahead we have  iterated through each group and through each student in the groups. Then we have checked if the group size is preference of student if not we are adding 2 to total cost and conflicting cost of each student. Then for each not wanted member is in the group if it’s there we are adding 10 to the total cost and conflicting cost for each conflicting members. Also, if any wanted member is in any group if it’s there, we are adding 3 to conflicting cost and total cost for each member. Moving ahead we have added the conflicting cost of student to conflicting list. We have returned a tuple of total cost and conflicting cost dictionary. 

We have created a method for getting the successor states depending on the conflicting student. We have initialized a successor groups list. Then we have iterated through each row for changing position of conflicting student, if the row has conflicting student, then we will make a deep copy of the current state and store it in the successor_group. Moving ahead we have popped off the element from the group and made a new group from it, if after popping, the group becomes empty then we are not taking new state as valid state, else if row didn’t have a conflicting student, we have iterated to each student in that group and swapped the conflicting student with each student and making all swaps as new state. We have made a deep copy of the current assignment, swapped the conflicting student and appended state into the successor groups list. If the length of the group is not 3, we will add the conflicting student to this group and make a new state. Then we have returned the successor groups. In the solver function we have parsed the input file to get the student preferences and name. Then we have initialized empty lists for assigning groups. Now, we have iterated through each student and put them into a group of three minimizing the assignment checking cost. Further, we have calculated the total cost and the conflicting cost of each student in the dictionary. We had set the total cost as the current cost to compare.  Then we have yielded the first assigned group and its cost. Now we have stored the conflicting costs by extracting the keys from the initial dictionary and then we have found the student with the maximum conflicting cost. If any other student has the same conflicting cost, we will assign it back to the dictionary. We have then calculated the time for the local cost. Now in a while loop, we have found the most conflicting student and then got all the successor states of the assigned group by changing position of most conflicting student. Now, iterating through each successor state, we have extracted the cost of successor and conflicting cost of students in successors state. We have then checked if the cost is less than current cost if yes, then yielding the new assigned group and cost. If the time of setting the most conflicting student is greater than 20, we have reinitialized the groups and taken the second most conflicting cost. If the time doesn’t reach 20, then we have checked the conflicting student from successor states.
