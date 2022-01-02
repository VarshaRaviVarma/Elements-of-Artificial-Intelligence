ELEMENTS OF ARTIFICIAL INTELLIGENCE

# ASSIGNMENT 0

# **REPORT**

## VARSHA RAVI VARMA
## 2000751388


######################################### QUESTION 1

Question 1 involves a problem which asks us to find a solution that includes finding the path and the path distance taken by the bird pichu from the initial state (p) to the goal state (@), given a few conditions such as open path (.) and closed path (x) in the grid. This problem involves consideration of concepts such as BFS, DFS, A\* and fringe. Now I will elaborate on the approach I took for solving this problem.

## Observation

Firstly, I ran the skeleton code given on the github repository to check what the output of the algorithm looked like initially. The output was an infinite loop that displayed “Shhhh... quiet while I navigate! “.

I then started analysing the algorithm function wise to understand the flow of the given code.

def parse_map(filename)- Function used to read the file used for this problem.
def valid_index(pos, n, m)- Function to check if that particular row and column is in the grid and not out of bound.
def moves(map, row, col)- Function used to find the next possible move.
def search(house_map)- Function to search the path and path count. This is where I have to work on the code to make it work and get the expected output.
if __name__ == "__main__"- Main function used to call the maps and search function. 


## Approach and design decisions

I first tried figuring out the reason behind the algorithm giving an infinite loop output. The reason why that was the case was because the algorithm did not involve keeping a track of the path (no visited node/track record of the visited path). I created a visited set that keeps track of the visited path (visited = set()). I added visited.add(curr_move)in the while loop to add the visited path into the set. I edited the fringe related code lines such as fringe=[(pichu_loc,0,'')] where I added a blank string element to store the output path and fringe.append((move, curr_dist + 1, new_move_string))to append the new distance and path into fringe. I had to add 0 for the index value for the code to work precisely - (curr_move, curr_dist, move_string)=fringe.pop(0). 

In the ‘for’ loop within the search function, the algorithm uses an if-else statement to traverse through the grid after checking the current visited condition set by me. The if condition if house_map[move[0]][move[1]]=="@": checks if the agent has reached the goal state. If the agent did reach the goal state, the path and the path count is being returned. In move_count = curr_dist + 1 , +1 is taken as the count of the agent taking the goal’s position. return (move_count, move_string) returns the output of the program. If the above ‘if’ condition is not met,  then it means that the newly visited path is being appended and is being tracked by using the code fringe.append((move, curr_dist + 1, new_move_string)).

Prior to displaying the path, I defined a new function def path(curr_move, row, col)in which I am using an if-else statement to check if the agent moved up, down, right or left in the grid. To check this, I am finding the difference in location between the previous move and the current location of the agent by subtracting both their values. If there is any difference in rows, it means the agent moved up or down and if there is any difference in columns, it means the agent moved to the left or right in the grid. 


### Challenges

The above elaborated explanation was of how I approached the problem at the start and what solution I came up with at the end. It goes without saying that I definitely did face at least a few challenges with my approach strategy before getting the right output. Let’s take a look at what challenges I faced before getting the expected output.  

Which concept to use for the given problem? BFS, DFS or A*? I first tried solving the problem using DFS which failed due to the output going into an infinite loop every time the program was run. I  changed the code from DFS and made it BFS which ended up working as I hoped it would.

It didn’t take me long enough to realise that depending only on the visited set and ignoring the proper use of fringe would lead me with the wrong output. I tried maintaining the fringe as it is without altering it and tried using only the visited set that gave me an output with the right path count but wrong path. The pathcount was right because I extracted it using fringe but the path was wrong since I totally ignored the fringe while extracting the path. I then made necessary changes to the fringe and finally got the expected output.

The concept of directions (U,D,R,L) used to display the path might be an easy part to implement but I must say I did get confused for a bit regarding the same. I tried implementing it in the search function but it seemed a bit confusing to implement the whole thing into the nested loops of the search function. Therefore, I decided to create a different function for the directions of the path and call it in the search function to make the code look more organised and easy to understand.

After all the necessary changes were made to rectify the above-mentioned errors, I was expecting the code to run without any issues since I did not find any error in the logic. Yes, the code failed to give the expected result though there was no logical error made. Trying to figure out this error was the most challenging one. I used move_string += path(curr_move,move[0],move[1]) to store the path at first. Took me a few minutes to realise that the error was “+=” since strings in python are immutable (yes, I am new to python). I replaced the above line of code with new_move_string = move_string + path(curr_move,move[0],move[1]) and the code worked perfectly and the expected output was displayed precisely for the first time . A moment of rejoice indeed.


### Input

Map 1:

16

True

4

....XXX

.XXX...

....X..

.X.X...

.X.X.X.

pX...X@

### Output

Shhhh... quiet while I navigate!

Here&#39;s the solution I found:

16 UUURRDDDRRUURRDD

### Conclusion

The algorithm was fixed and the expected output was obtained.










############################# QUESTION 2

Question 1 involved a problem that asks us to find a solution that includes finding the path and the path distance taken by the bird pichu from the initial state (p) to the goal state (@), given a few conditions such as open path (.) and closed path (x) in the grid. But in question 2, we have multiple other factors to consider before getting into coding the search function.

According to the question, we understand the following:
There are multiple agents (k) present in the grid at the same time and a parameter has to be specified in the code that holds the value of k. Also, assume k>=1.
These agents can not stand each other and therefore can not be placed directly facing each other in the grid. Any 2 agents can not be placed in the same row, column or even diagonally. 
X is considered to represent a wall in the grid. The condition is such that 2 agents can be placed in the same row, column or diagonally only and only if there is a wall between them on the grid.
Agents can be positioned only at empty squares (.) and not on the wall squares (x). Therefore, we understand that the positions of x are immovable.
You are represented as @ on the grid and you have the same characteristics/conditions as that of a wall (x).
Agents are to be represented as ‘p’ on the map/grid.


## Observation

Firstly, I ran the skeleton code given on the github repository to check what the output of the algorithm looked like initially. The output displayed the following error: “File "arrange_pichus.py", line 55, in <module>\n k = int(sys.argv[2])\n IndexError: list index out of range“.
  
I then started analysing the algorithm function wise to understand the flow of the given code. 

def parse_map(filename)- Function used to read the file used for this problem.
def count_pichus(house_map)- Function to check and count the total number of agents (k) available on the map.
def printable_house_map(house_map)- Function used to print the map.
def add_pichu(house_map, row, col)- Function to add the bird to a new position on the map.
def successors(house_map)- Function used to add pichu on the map.
def is_goal(house_map, k)- Function to check and compare if the map achieved is the goal state or not.
def solve(initial_house_map,k)- Function that contains fringe and return statement of the output.
if __name__ == "__main__"- Main function used to call the maps and solve function. 


## Approach and design decisions

The approach I considered is that of a N queen problem with special conditions such as walls (x). My logical design of the solution is to first place the pichu at one safe valid place (initial location), traverse through the grid and search square by square if it is a valid place for the next agent to be placed. This leads us to building a code that checks if the agent is directly facing any other agent.

I defined a check function def check(house_map, row, col): that checks if there is any agent directly placed facing another agent. To check the row, I have used the following code that checks if there is already an agent present in the same row:

for i in range(col):
       if house_map[row][i] == 'p':
           return False
           
To check the column:
for i in range(row):
       if house_map[i][col] == 'p':
           return False
           
To check the diagonals:
   for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
       if house_map[i][j] == 'p':
           return False
  for i, j in zip(range(row, k, 1), range(col, -1, -1)):
       if house_map[i][j] == 'p':
           return False
           
The idea is if there is another agent facing the current agent, it returns false otherwise returns true. If true is returned, then place the agent in that location and repeat the loop for a new agent to be placed in the map. The loop repeats until there can be no more ‘p’ placed on the map. 

While searching for a valid location for the agent, we need to also check for the walls (x) that are positioned in the maps. We need to condition the program in a way that if the agent faces the wall before facing the agent in the same row, column and diagonals, it considers the location to be valid, whereas it returns false if it faces the agent directly. We also need to place a condition stating you are the same as a wall in the map (@=x). 
Check function to be called inside the solve function to perform the grid search.

### Challenges

The above elaborated explanation was for how I approached the problem at the start and what solution I came up with at the end. It goes without saying that I definitely did face at least a few challenges with my approach strategy before getting the right output. Let’s take a look at what challenges I faced before getting the expected output.  

Understanding the successors function was a little confusing at the start but when I tried breaking down the add_pichu line of code, I could understand how that is a very useful function throughout the algorithm.

Trying to code the part of the program to find the diagonals was challenging. As a beginner in python, it did pose as a great challenge to understand how the looping for the same works. Thus, I did look it up on the internet for the diagonal part of the code. I referred to websites such as ‘Stack Overflow’ and ‘GeeksForGeeks’.

As a beginner to python, I am finding it really hard to code the logic I have thought about in a code like manner. Understanding the question and coming up with the logic is not a challenge for me but implementing the logic into the skeleton code is complicated.

Relating the solve function and check function to properly work together.
