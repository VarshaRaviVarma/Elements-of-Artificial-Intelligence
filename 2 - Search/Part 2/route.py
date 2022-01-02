#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: [Aman Chaudhary(amanchau), Himanshu Bansal(hhimanshu), Varsha Ravi Verma(vravi)]
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
import sys
import math

# Method for reading and  parsing road-segment.txt
def parse_map(filename):

        # Opening the file and reading it
        with open(filename, "r") as f:

                # Making each road segment as list
                return [line.split(" ") for line in f.read().split("\n")]

# Method for reading and parsing city gps file
def parse_city_gps(filename):

    # Making a empty cities dictionary
    cities = {}

    # Opening the file and reading it
    with open(filename, "r") as f:

        # Reading each line and splitting it taking city name as key and lang and lat as value
        for line in f.read().split("\n"):
            city = line.split(" ")
            if(len(city) != 1):
                cities[city[0]] = [city[1], city[2]]
    return cities

# Calculating eucledian distance for heuristic value
def calc_euclidean(end_city_long,end_city_lat,current_city_long,current_city_lat):
        #Euclidean distance returned as the heuristic value
        return math.sqrt((float(end_city_long) - float(current_city_long)) ** 2 + (float(end_city_lat) - float(current_city_lat)) ** 2)

# Getting all the cities which are connected to current city via a highway segment
def get_successor_cities(current_city,roadsegment_map):

    # returning list of cities which have current city on either side of its highway end 
    return [city for city in roadsegment_map if city[0] == current_city or city[1] == current_city]

# Method for calculating delivery hours
def calc_delivery_hours(length, time_segment, time_trip):

    # Finding probability 
    p = math.tanh(length/1000)
    return time_segment + p * ( 2 * (time_segment + time_trip))

# Method for calculating heuristic value for time
def calc_time_heuristic(average_speed, eucledian_distance):
    return eucledian_distance/average_speed

# Method for calculating heuristic cost for segment
def calc_segment_heuristic(average_length, eucledian_distance):
    return eucledian_distance/average_length

# Method for calculating route based on distance function
def get_route_dist(start, end, roadsegment_map, citygps_dictionary):

    # Calculating heuristic cost of initial city
    euclid_dist = calc_euclidean(citygps_dictionary[start][0], citygps_dictionary[start][1], citygps_dictionary[end][0], citygps_dictionary[end][1])
    
    # Implementing fringe in form of priority queue using dictionary of python (Setting cost as key and a list(all the coordinates with same cost) of tupples(current_city, current_segment, current_distance, current_hours, current_deliveryhours, current_route) as value)
    fringe = {euclid_dist: [(start, 0 , 0 , 0, 0, [])]}
    
    # Initialising visited highway map
    visited_city = []

    while (fringe):
        # Extracting the keys from the dictioanry and storing them as priority
        priority = fringe.keys()
        # Storing the minimum value from the keys in min_priority
        min_priority = min(priority)
        # Popping off the minimum priority from the fringe
        min_priority_city = fringe.pop(min_priority)
        # Extracting the values from the min_priority_city and appending it to the fringe
        (current_city, current_segment, current_distance, current_hours, current_deliveryhours, current_route) = min_priority_city[0]

        min_priority_city = min_priority_city[1:]

        # Checking if the length of the min_priority is not equal to 0
        if (len(min_priority_city) != 0):
            # Replacing the min_priority in the fringe
            fringe[min_priority] = min_priority_city
        
        # Iterating over the successor states
        for city in get_successor_cities(current_city, roadsegment_map):
            # Condition to check if there are more than one highways between two cities
            if (city[0], city[1]) in visited_city or (city[1], city[0]) in visited_city:
                continue
            # Appending the city to the visited_city list
            visited_city.append((city[0], city[1]))
            # Initialzing the new city empty string
            new_city = ""
            old_city = ""
            # If city[0] is not the current city
            if city[0] != current_city:
                # Append city[0] to the new city string
                new_city = city[0]    
                old_city = city[1]     
            else:
                # Append city[1] to the new city string
                new_city = city[1]
                old_city = city[0]
            
            # Appending the new city with the highway name and the segment length to the current_route
            current_route.append((new_city,  city[4] + " for " + city[2] + " miles"))
            # Calculating the delivery hours by adding the current delivery hours to the average time to travel for a segment by dividing the segment length by the speed on the segment
            delivery_hours = current_deliveryhours + float(city[2])/float(city[3])
            # Condition to check if the  speed on the segment is greater than or equal to 50
            if float(city[3]) >= 50:
                # Devlivery hours is sum of current delivery hours with the time returned by the function cal_delivery_hours when the segment length, avg speed on segment and the current delivery hours are passed
                delivery_hours = current_deliveryhours + calc_delivery_hours(float(city[2]), float(city[2])/float(city[3]), current_deliveryhours)
            # Condition to check if we have reaached the end city
            if city[0] == end or city[1] == end:
                return {"total-segments" : current_segment + 1, 
                "total-miles" : current_distance + float(city[2]), 
                "total-hours" : current_hours + float(city[2])/float(city[3]), 
                "total-delivery-hours" : delivery_hours, 
                "route-taken" : current_route}
            # Condition to check if the new city is in the citygps dictionary
            if new_city in citygps_dictionary:
                # Calculating the euclidean distance between the cities and adding it to the current distance
                euclid_dist = current_distance + float(city[2]) + calc_euclidean(citygps_dictionary[end][0], citygps_dictionary[end][1], citygps_dictionary[new_city][0], citygps_dictionary[new_city][1])
            elif old_city in citygps_dictionary:
                euclid_dist = current_distance + calc_euclidean(citygps_dictionary[end][0], citygps_dictionary[end][1], citygps_dictionary[old_city][0], citygps_dictionary[old_city][1])
            else:
                euclid_dist = calc_euclidean(citygps_dictionary[end][0], citygps_dictionary[end][1], citygps_dictionary[start][0], citygps_dictionary[start][1])
            if euclid_dist in fringe:
                fringe[euclid_dist].append((new_city, current_segment + 1, current_distance + float(city[2]), current_hours + float(city[2])/float(city[3]), delivery_hours, current_route))
            else:
                fringe[euclid_dist] = [(new_city, current_segment + 1, current_distance + float(city[2]), current_hours + float(city[2])/float(city[3]), delivery_hours, current_route)]
            current_route = current_route[:len(current_route)-1]

# Method for calculating route based on segment
def get_route_segment(start, end, roadsegment_map, citygps_dictionary):
    
    # Intitializing the average length as 0
    average_length = 0
    
    # Adding the length of the segment to the average length
    for road in roadsegment_map:
        average_length += float(road[2])
    
    # Division of average length with the size of the roadsegment map gives the average length
    average_length = average_length/len(roadsegment_map)
    
    # Calculating the euclidean distance as the heuristic value
    euclid_dist = calc_euclidean(citygps_dictionary[start][0], citygps_dictionary[start][1], citygps_dictionary[end][0], citygps_dictionary[end][1])
    
    # Initialzing the fringe
    fringe = {}

    # Calling the calc_segment_heuristic function and storing it in the heuristic segments functions
    heuristic_segments = 0

    # Implementing fringe in form of priority queue using dictionary of python (Setting cost as key and a list(all the coordinates with same cost) of tupples(current_city, current_segment, current_distance, current_hours, current_deliveryhours, current_route) as value)
    fringe[heuristic_segments] = [(start, 0 , 0 , 0, 0, [])]

    # Initialising Visited highway map
    visited_city = []

    while fringe:
        # Extracting the keys from the dictioanry and storing them as priority
        priority = fringe.keys()
        # Storing the minimum value from the keys in min_priority
        min_priority = min(priority)
        # Popping off the minimum priority from the fringe
        min_priority_city = fringe.pop(min_priority)
        # Extracting the values from the min_priority_city and appending it to the fringe
        (current_city, current_segment, current_distance, current_hours, current_deliveryhours, current_route) = min_priority_city[0]

        min_priority_city = min_priority_city[1:]

        # Checking if the length of the min_priority is not equal to 0
        if (len(min_priority_city) != 0):
            # Replacing the min_priority in the fringe
            fringe[min_priority] = min_priority_city
        # Iterating over the successor states
        for city in get_successor_cities(current_city, roadsegment_map):
            # Condition to check if there are more than one highways between two cities
            if (city[0], city[1]) in visited_city or (city[1], city[0]) in visited_city:
                continue
            # Appending the city to the visited_city list
            visited_city.append((city[0], city[1]))
            # Initialzing the new city empty string
            new_city = ""
            # If city[0] is not the current city
            if city[0] != current_city:
                # Append city[0] to the new city string
                new_city = city[0]         
            else:
                # Append city[1] to the new city string
                new_city = city[1]
            
            # Appending the new city with the highway name and the segment length to the current_route
            current_route.append( (new_city,  city[4] + " for " + city[2] + " miles"))
            # Calculating the delivery hours by adding the current delivery hours to the average time to travel for a segment by dividing the segment length by the speed on the segment
            delivery_hours = current_deliveryhours + float(city[2])/float(city[3])
            # Condition to check if the  speed on the segment is greater than or equal to 50
            if float(city[3]) >= 50:
                # Devlivery hours is sum of current delivery hours with the time returned by the function cal_delivery_hours when the segment length, avg speed on segment and the current delivery hours are passed
                delivery_hours = current_deliveryhours + calc_delivery_hours(float(city[2]), float(city[2])/float(city[3]), current_deliveryhours)
            # Condition to check if we have reaached the end city
            if city[0] == end or city[1] == end:
                return {"total-segments" : current_segment + 1, 
                "total-miles" : current_distance + float(city[2]), 
                "total-hours" : current_hours + float(city[2])/float(city[3]), 
                "total-delivery-hours" : delivery_hours, 
                "route-taken" : current_route}
            # Condition to check if the new city is in the citygps dictionary    
            if new_city in citygps_dictionary:
                # Calculating the euclidean distance between the cities and adding it to the current distance
                heuristic_segment = current_segment +  2
            else:
                heuristic_segment = current_segment + 2
            if heuristic_segment in fringe:
                fringe[heuristic_segment].append((new_city, current_segment + 1, current_distance + float(city[2]), current_hours + float(city[2])/float(city[3]), delivery_hours, current_route))
            else:
                fringe[heuristic_segment] = [(new_city, current_segment + 1, current_distance + float(city[2]), current_hours + float(city[2])/float(city[3]), delivery_hours, current_route)]
            current_route = current_route[:len(current_route)-1]

# Method for calculating route based on time
def get_route_time(start, end, roadsegment_map, citygps_dictionary):
    # Intitializing the average length as 0
    average_speed = 0
    # Initialising visited cities list
    visited_city = []
    # Adding the length of the segment to the average length
    for road in roadsegment_map:
        average_speed += float(road[3])
    # Division of average length with the size of the roadsegment map gives the average length
    average_speed = average_speed/len(roadsegment_map)
    # Calculating the euclidean distance as the heuristic value
    euclid_dist = calc_euclidean(citygps_dictionary[start][0], citygps_dictionary[start][1], citygps_dictionary[end][0], citygps_dictionary[end][1])
    # Calling the calc_time_heuristic function and storing it in the heuristic time function
    heuristic_time = calc_time_heuristic(average_speed, euclid_dist)
    # Initializing the fringe
    fringe = {}
    # Implementing fringe in form of priority queue using dictionary of python (Setting cost as key and a list(all the coordinates with same cost) of tupples(current_city, current_segment, current_distance, current_hours, current_deliveryhours, current_route) as value)
    fringe[heuristic_time] = [(start, 0 , 0 , 0, 0, [])]

    while (fringe):
        # Extracting the keys from the dictioanry and storing them as priority
        priority = fringe.keys()
        # Storing the minimum value from the keys in min_priority
        min_priority = min(priority)
        # Popping off the minimum priority from the fringe
        min_priority_city = fringe.pop(min_priority)
        # Extracting the values from the min_priority_city and appending it to the fringe
        (current_city, current_segment, current_distance, current_hours, current_deliveryhours, current_route) = min_priority_city[0]

        min_priority_city = min_priority_city[1:]

        # Checking if the length of the min_priority is not equal to 0
        if (len(min_priority_city) != 0):
            # Replacing the min_priority in the fringe
            fringe[min_priority] = min_priority_city
        
        # Iterating over the successor states
        for city in get_successor_cities(current_city, roadsegment_map):
            # Condition to check if there are more than one highways between two cities
            if (city[0], city[1]) in visited_city or (city[1], city[0]) in visited_city:
                continue
            # Appending the city to the visited_city list
            visited_city.append((city[0], city[1]))
            # Initialzing the new city empty string
            new_city = ""
            old_city = ""
            # If city[0] is not the current city
            if city[0] != current_city:
                # Append city[0] to the new city string
                new_city = city[0]  
                old_city = city[1]       
            else:
                # Append city[1] to the new city string
                new_city = city[1]
                old_city = city[0]
            
            # Appending the new city with the highway name and the segment length to the current_route
            current_route.append( (new_city,  city[4] + " for " + city[2] + " miles"))
            # Calculating the delivery hours by adding the current delivery hours to the average time to travel for a segment by dividing the segment length by the speed on the segment
            delivery_hours = current_deliveryhours +  float(city[2])/float(city[3])
            # Condition to check if the  speed on the segment is greater than or equal to 50
            if float(city[3]) >= 50:
                # Delivery hours is sum of current delivery hours with the time returned by the function cal_delivery_hours when the segment length, avg speed on segment and the current delivery hours are passed
                delivery_hours = current_deliveryhours + calc_delivery_hours(float(city[2]), float(city[2])/float(city[3]), current_deliveryhours)
            # Condition to check if we have reached the end city
            if city[0] == end or city[1] == end:
                return {"total-segments" : current_segment + 1, 
                "total-miles" : current_distance + float(city[2]), 
                "total-hours" : current_hours + float(city[2])/float(city[3]), 
                "total-delivery-hours" : delivery_hours, 
                "route-taken" : current_route}
            # Condition to check if the new city is in the citygps dictionary  
            if new_city in citygps_dictionary:
                # Calculating the euclidean distance between the cities and adding it to the current distance
                euclid_dist = calc_euclidean(citygps_dictionary[end][0], citygps_dictionary[end][1], citygps_dictionary[new_city][0], citygps_dictionary[new_city][1])
                heuristic_time = current_hours +  float(city[2])/float(city[3]) + calc_time_heuristic(average_speed, euclid_dist)
            elif old_city in citygps_dictionary:
                euclid_dist = calc_euclidean(citygps_dictionary[end][0], citygps_dictionary[end][1], citygps_dictionary[old_city][0], citygps_dictionary[old_city][1]) - float(city[2])
                heuristic_time = current_hours + float(city[2])/float(city[3]) + calc_time_heuristic(average_speed, euclid_dist)
            else:
                euclid_dist = calc_euclidean(citygps_dictionary[end][0], citygps_dictionary[end][1], citygps_dictionary[start][0], citygps_dictionary[start][1]) - float(city[2]) - current_distance
                heuristic_time = current_hours + float(city[2])/float(city[3]) + calc_time_heuristic(average_speed, euclid_dist)
            if heuristic_time in fringe:
                fringe[heuristic_time].append((new_city, current_segment + 1, current_distance + float(city[2]), current_hours + float(city[2])/float(city[3]), delivery_hours, current_route))
            else:
                fringe[heuristic_time] = [(new_city, current_segment + 1, current_distance + float(city[2]), current_hours + float(city[2])/float(city[3]), delivery_hours, current_route)]
            current_route = current_route[:len(current_route)-1]

# Method for calculating route based on hours
def get_route_del_hours(start, end, roadsegment_map, citygps_dictionary):
    # Intitializing the average length as 0
    average_speed = 0
    # Initialising visited cities list
    visited_city = []
    # Adding the length of the segment to the average length
    for road in roadsegment_map:
        average_speed += float(road[3])
    # Division of average length with the size of the roadsegment map gives the average length
    average_speed = average_speed/len(roadsegment_map)
    # Calculating the euclidean distance as the heuristic value
    euclid_dist = calc_euclidean(citygps_dictionary[start][0], citygps_dictionary[start][1], citygps_dictionary[end][0], citygps_dictionary[end][1])
    # Calling the calc_time_heuristic function and storing it in the heuristic time function
    heuristic_del_time = calc_time_heuristic(average_speed, euclid_dist)
    # Initializing the fringe
    fringe = {}
    # Implementing fringe in form of priority queue using dictionary of python (Setting cost as key and a list(all the coordinates with same cost) of tupples(current_city, current_segment, current_distance, current_hours, current_deliveryhours, current_route) as value)
    fringe[heuristic_del_time] = [(start, 0 , 0 , 0, 0, [])]

    while (fringe):
        # Extracting the keys from the dictioanry and storing them as priority
        priority = fringe.keys()
        # Storing the minimum value from the keys in min_priority
        min_priority = min(priority)
        # Popping off the minimum priority from the fringe
        min_priority_city = fringe.pop(min_priority)
        # Extracting the values from the min_priority_city and appending it to the fringe
        (current_city, current_segment, current_distance, current_hours, current_deliveryhours, current_route) = min_priority_city[0]

        min_priority_city = min_priority_city[1:]

        # Checking if the length of the min_priority is not equal to 0
        if (len(min_priority_city) != 0):
            # Replacing the min_priority in the fringe
            fringe[min_priority] = min_priority_city
        
        # Iterating over the successor states
        for city in get_successor_cities(current_city, roadsegment_map):
            # Condition to check if there are more than one highways between two cities
            if (city[0], city[1]) in visited_city or (city[1], city[0]) in visited_city:
                continue
            # Appending the city to the visited_city list
            visited_city.append((city[0], city[1]))
            # Initialzing the new city empty string
            new_city = ""
            # If city[0] is not the current city
            if city[0] != current_city:
                # Append city[0] to the new city string
                new_city = city[0]         
            else:
                # Append city[1] to the new city string
                new_city = city[1]
            
            # Appending the new city with the highway name and the segment length to the current_route
            current_route.append( (new_city,  city[4] + " for " + city[2] + " miles"))
            # Calculating the delivery hours by adding the current delivery hours to the average time to travel for a segment by dividing the segment length by the speed on the segment
            delivery_hours = current_deliveryhours +  float(city[2])/float(city[3])
            # Condition to check if the  speed on the segment is greater than or equal to 50
            if float(city[3]) >= 50:
                # Delivery hours is sum of current delivery hours with the time returned by the function cal_delivery_hours when the segment length, avg speed on segment and the current delivery hours are passed
                delivery_hours = current_deliveryhours + calc_delivery_hours(float(city[2]), float(city[2])/float(city[3]), current_deliveryhours)
            # Condition to check if we have reached the end city
            if city[0] == end or city[1] == end:
                return {"total-segments" : current_segment + 1, 
                "total-miles" : current_distance + float(city[2]), 
                "total-hours" : current_hours + float(city[2])/float(city[3]), 
                "total-delivery-hours" : delivery_hours, 
                "route-taken" : current_route}
            
            # Condition to check if the new city is in the citygps dictionary  
            if new_city in citygps_dictionary:
                # Calculating the euclidean distance between the cities and adding it to the current distance
                euclid_dist = current_distance + calc_euclidean(citygps_dictionary[end][0], citygps_dictionary[end][1], citygps_dictionary[new_city][0], citygps_dictionary[new_city][1])
                heuristic_del_time = delivery_hours + calc_time_heuristic(average_speed, euclid_dist)
            else:
                euclid_dist = current_distance
                heuristic_del_time = delivery_hours + calc_time_heuristic(average_speed, euclid_dist)
            if heuristic_del_time in fringe:
                fringe[heuristic_del_time].append((new_city, current_segment + 1, current_distance + float(city[2]), current_hours + float(city[2])/float(city[3]), delivery_hours, current_route))
            else:
                fringe[heuristic_del_time] = [(new_city, current_segment + 1, current_distance + float(city[2]), current_hours + float(city[2])/float(city[3]), delivery_hours, current_route)]
            current_route = current_route[:len(current_route)-1]
    

def get_route(start, end, cost):
    
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    # Parsing and storing roadsegment map
    roadsegment_map = parse_map("./road-segments.txt")
    roadsegment_map = roadsegment_map[:len(roadsegment_map)-1]
    # Parsing and storing citygps map
    citygps_dictionary = parse_city_gps("./city-gps.txt")
    # If distance is passed in the cost function
    if (cost == "distance"):
        return get_route_dist(start, end, roadsegment_map, citygps_dictionary)
    # If segments is passed in the cost function
    elif (cost == "segments"):
        return get_route_segment(start, end, roadsegment_map, citygps_dictionary)
    # If time is passed in the cost function
    elif (cost == "time"):
        return get_route_time(start, end, roadsegment_map, citygps_dictionary)
    # Else pass delivery hours in the cost function
    else:
        return get_route_del_hours(start, end, roadsegment_map, citygps_dictionary)


# Please don't modify anything below this line
#
if __name__ == "__main__":
    
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))
    #print(calc_euclidean(citygps_dictionary[start_city][0], citygps_dictionary[start_city][1], citygps_dictionary[end_city][0], citygps_dictionary[end_city][1]))
    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])
 


