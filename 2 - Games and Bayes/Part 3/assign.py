 #!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

from math import cos
import sys
import time
import copy

# Method to read the input file and storing data
def parse_input_file(filename):

    # Initialising the preferences dictionary for storing all the preference of each student
    preferences = {}

    # Initialising a list for storing all the students
    students = []

    # Reading file containing all student data
    with open(filename, "r") as f:

        # Traversing through each line of file
        for line in f.read().split("\n"):

            # Spliting each line by spaces to get all the answers entered by a student (studentName, team members wanted, team members not wanted)
            preference = line.split(" ")
            
            # handling the last line in text file
            if(len(preference) != 1):

                # Retrieving Wanted Team Members which is at index 1 and spliiting it by "-" and getting the rest list of members
                wanted_team_members = preference[1].split("-")[1:]

                # Calculating how much team members required by student
                no_team_members = len(wanted_team_members) + 1

                # Check if zzz or xxx is in wanted members list and removing it
                if "zzz" in wanted_team_members:
                    wanted_team_members = [wanted_team_member for wanted_team_member in wanted_team_members if wanted_team_member != "zzz"]
                if "xxx" in wanted_team_members:
                    wanted_team_members = [wanted_team_member for wanted_team_member in wanted_team_members if wanted_team_member != "xxx"]
                
                # Retrieving the not wanted team members and spliting by "," 
                not_wanted_team_members = preference[2].split(",")
                
                # Checking if _ is present in not wanted member list so removing it
                if "_" in not_wanted_team_members:
                    not_wanted_team_members.remove("_")

                # Adding student details to dictionary
                preferences[preference[0]] = {"no_team_members": no_team_members, "wanted_team_members":wanted_team_members, "not_wanted_team_members": not_wanted_team_members}
                
                # Appending student name to student list
                students.append(preference[0])
    
    # Returning Tupple containing prefrences of students and students list
    return (preferences, students)

# finding the student row and column of student having most conflicting cost in assigned groups
def find_conflict_student(assigned_groups, student):

    # Iterating to every row and if student is in that row finding column in particular row and returning (row, column)
    for row in range(len(assigned_groups)):
        if student in assigned_groups[row]:
            col = assigned_groups[row].index(student)
            return (row, col)

# Calculating the cost of assigned groups and conflicting cost of each student
def calc_cost(assigned_groups, preferenceMap):

    # making a dictionary of conflicting with student name
    dict_conflicting_cost = {}

    # Initialising cost with numbers of groups into 5
    cost = len(assigned_groups) * 5
    
    # Iterating through each group
    for assigned_group in assigned_groups:

        # Iterating through each student in the group 
        for student in assigned_group:
            
            # Initialising the conflicting cost for each student to 0
            conflicting_cost = 0

            # Checking if the group size is prefernce of student if not we are adding 2 to total cost and conflicting cost of each student
            if preferenceMap[student]["no_team_members"] != len(assigned_group):
                cost +=  2
                conflicting_cost += 2
            
            # Checking for each not wanted member is in the group if its there we are adding 10 to the total cost and conflicting cost for each conflicting members
            for not_wanted_team_member in preferenceMap[student]["not_wanted_team_members"]:
                if not_wanted_team_member in assigned_group:
                    cost += 10
                    conflicting_cost += 10
            
            # Checking if any wanted member is in any group if its there we are adiing 3 to conflicting cost and total cost for each member 
            for wanted_team_member in preferenceMap[student]["wanted_team_members"]:
                if wanted_team_member not in assigned_group:
                    cost += 3
                    conflicting_cost += 3

            # Adding the conflicting cost of student to conflicting list
            if(conflicting_cost in dict_conflicting_cost):
                dict_conflicting_cost[conflicting_cost].append(student)
            else:
                dict_conflicting_cost[conflicting_cost] = [student]
    
    # returning total cost  and conflicting cost dictionary
    return (cost, dict_conflicting_cost)

# Method for getting successor states depending on conflicting student
def get_successor_state(assigned_groups, conflicting_student_row, conflicting_student_col):

    # Initialising successor groups list
    successor_groups =[]
    
    # Iterating each row for changing position of conflicting student
    for row in range(len(assigned_groups)):

        # If row has conflicting student
        if row == conflicting_student_row:

            # Making a deep copy of current state
            successor_group = copy.deepcopy(assigned_groups)

            # Popping element from group and making a new group from it and the new state into list 
            # if after popping group becomes empty then we are not taking new state valid state
            student = successor_group[row].pop(conflicting_student_col)
            if len(successor_group[row]) != 0:
                successor_group.append([student])
                successor_groups.append(successor_group)
        else:

            # If row does not had conflicting student
            # Iterating to each student in that group and swapping the conflicting student with each student and making all swaps as new state
            for col in range(len(assigned_groups[row])):

                # making deep copy of current assignment
                successor_group = copy.deepcopy(assigned_groups)

                # swapping conflicting student
                temp = successor_group[conflicting_student_row][conflicting_student_col]
                successor_group[conflicting_student_row][conflicting_student_col] = successor_group[row][col]
                successor_group[row][col] = temp

                # appending state into successor groups list
                successor_groups.append(successor_group)

            # if length of group is not 3 we will add the conflicting student to this group and make a new state
            if len(assigned_groups[row]) != 3:
                successor_group = copy.deepcopy(assigned_groups)
                student = successor_group[conflicting_student_row].pop(conflicting_student_col)
                successor_group[row].append(student)
                if(len(successor_group[conflicting_student_row]) == 0):
                    successor_group.pop(conflicting_student_row)
                successor_groups.append(successor_group)

    # returning all sucessor states
    return successor_groups

# it is main solver function 
def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """
  
    # This solution will never befound, but that's ok; program will be killed eventually by the
    #  test script.
    
    # Parsing the input file ang getting student preferences and name
    (preferences, students) = parse_input_file(input_file)

    # Initialising empty list for assigning groups 
    assigned_groups = []
    assigned_group = []

    # Iterating through each student and putting them into a group of three minimising the assignment checking cost
    for student in students:
        if len(assigned_group) == 3:
            assigned_groups.append(assigned_group)
            assigned_group = []
        assigned_group.append(student)
    assigned_groups.append(assigned_group)

    initial_assigned_groups = assigned_groups
    # Finding the total cost and conflicting cost of each student in a dictionary
    (cost, initial_dict_conflicting_cost) = calc_cost(assigned_groups, preferences)

    # setting the total cost as current cost to compare
    curr_cost = cost

    # Yeilding the first assigned group and its cost
    yield({"assigned-groups": ["-".join(group) for group in assigned_groups],
               "total-cost" : cost})
    
    # getting all the conflicting costs
    conflicting_cost_keys = initial_dict_conflicting_cost.keys()

    # getting maximum conflicting cost
    max_conflicting_cost = max(conflicting_cost_keys)

    # getting the student with most conflicting cost
    most_conflicting_students = initial_dict_conflicting_cost.pop(max_conflicting_cost)
    most_conflicting_student = most_conflicting_students.pop(0)

    # if anytother student with same conflicting cost is present assigning it back to dictionary
    if len(most_conflicting_students) != 0:
        initial_dict_conflicting_cost[max_conflicting_cost] = most_conflicting_students
    dict_most_conflicting_student =  initial_dict_conflicting_cost
    
    # Taking start time for locla cost
    start_time = time.time()

    # Running a infinite loop
    while True:

        # FInding row and column of most conflicting student
        (most_conflict_student_row, most_conflict_student_col) = find_conflict_student(assigned_groups, most_conflicting_student)
        
        # getting all the succesor states of assigned group by changing pos of most conflicting student
        successor_states = get_successor_state(assigned_groups, most_conflict_student_row, most_conflict_student_col)
        
        # Iterating through Each successor state
        for successor_state in successor_states:
            
            # getting cost of succesoor state and conflicting cost of students in successor state
            (cost, dict_most_conflicting_student) = calc_cost(successor_state, preferences)

            # checking cost is less than curr cost if yes then yielding the neww assigned group and cosr
            if cost < curr_cost:
                assigned_groups = successor_state
                curr_cost = cost
                yield({"assigned-groups": ["-".join(group) for group in assigned_groups],
               "total-cost" : cost})
        
        # if time of setting the most conflicting student is greater than 20 reintiallising the groups and taking second most conflicting student
        if time.time() - start_time > 20:
            if not initial_dict_conflicting_cost:
                break
            conflicting_cost_keys = initial_dict_conflicting_cost.keys()
            max_conflicting_cost = max(conflicting_cost_keys)
            most_conflicting_students = initial_dict_conflicting_cost.pop(max_conflicting_cost)
            most_conflicting_student = most_conflicting_students.pop(0)
            if len(most_conflicting_students) != 0:
                initial_dict_conflicting_cost[max_conflicting_cost] = most_conflicting_students
            dict_most_conflicting_student =  initial_dict_conflicting_cost
            assigned_groups = initial_assigned_groups
            start_time = time.time()
        else:
            # if time doesn't reach 20 then cheking conflicting student from successor state amd then working on it
            if not dict_most_conflicting_student:
                if not initial_dict_conflicting_cost:
                    break
                assigned_groups = initial_assigned_groups
                dict_most_conflicting_student = initial_dict_conflicting_cost
            conflicting_cost_keys = dict_most_conflicting_student.keys()
            max_conflicting_cost = max(conflicting_cost_keys)
            most_conflicting_students = dict_most_conflicting_student.pop(max_conflicting_cost)
            most_conflicting_student = most_conflicting_students.pop(0)
            if len(most_conflicting_students) != 0:
                dict_most_conflicting_student[max_conflicting_cost] = most_conflicting_students
        
    
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])