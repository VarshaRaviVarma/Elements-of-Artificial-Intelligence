# SeekTruth.py : Classify text objects into two categories
#
# PLEASE PUT YOUR NAMES AND USER IDS HERE!
# [Aman Chaudhary amanchau  Himanshu Himanshu hhimansh  Varsha Ravi Verma varavi]
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys
import string
import math

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
def classifier(train_data, test_data):
   
    # This is just dummy code -- put yours here!
   
   #dictionaries to store words and their count
    bag_of_words = {}
    bag_of_words_truthful = {}
    bag_of_words_deceptive = {}

    # list containing stop words
    stop_words = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']
    
    # storing each label and each comment into respective list
    objects = train_data["objects"]
    labels = train_data["labels"]

    # calculating probability of any comment being truthful or deceptive
    p_truthful = labels.count("truthful")/len(labels)
    p_deceptive = labels.count("deceptive")/len(labels)

    # iterating through each comment
    for i in range(len(objects)):
        
        # storing ith comment
        data = objects[i]
        
        # cleaning ith comment removing punctuations and numbers and making each character to lower case
        data = data.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
        data = ''.join(s for s in data if not s.isdigit())
        data = data.lower()

        # spliting ith comment to single(word) i.e. tokens
        data = data.split()
  
        # Storing label of ith comment
        label = labels[i]
 
        # Iterating through each token of comment
        for each_data in data:

            # checking if token is in stop_words if yes then continuing(not adding it to words buckets)
            if each_data in stop_words:
                continue

            # Checking if token already exist in bag of words if it is then increasing the count by 1 otherwise adding the word to bag
            if each_data in bag_of_words:
                bag_of_words[each_data] += 1
            else:
                bag_of_words[each_data] = 1

            # Checking if the label is truthful
            if label == "truthful":

                # Checking if token already exist in truthful bag of words if it is then increasing the 
                # count by 1 otherwise adding the  word to truthful bag
                if each_data in bag_of_words_truthful:
                    bag_of_words_truthful[each_data] += 1
                else:
                    bag_of_words_truthful[each_data] = 1
            else:

                # if label is not truthful then its deceptive 
                # Checking if token already exist in deceptive bag of words if it is then increasing the 
                # count by 1 otherwise adding the  word to deceptive bag
                if each_data in bag_of_words_deceptive:
                    bag_of_words_deceptive[each_data] += 1
                else:
                    bag_of_words_deceptive[each_data] = 1
    
    # making a list of keys from bag of words
    words = list(bag_of_words.keys())

    # Iterating through each key in bag of words
    for word in words:

        # checking if total count of any word is less than 20 if 
        # yes we are removing it from both deceptive and truthful word og bags
        if bag_of_words[word] < 20:
            if word in bag_of_words_truthful:
                bag_of_words_truthful.pop(word)
            if word in bag_of_words_deceptive:
                bag_of_words_deceptive.pop(word)
    
    # calculating total cummulitive frequency of word in bag of truthful words
    count_words = sum(list(bag_of_words_truthful.values()))

    # Iterating through each word in bag of truthful words finding its probability 
    for word in bag_of_words_truthful:
        bag_of_words_truthful[word] = bag_of_words_truthful[word]/count_words
    
    # calculating total cummulitive frequency of word in bag of deceptive words
    count_words = sum(list(bag_of_words_deceptive.values()))
    
    # Iterating through each word in bag of deceptive words finding its probability
    for word in bag_of_words_deceptive:
        bag_of_words_deceptive[word] = bag_of_words_deceptive[word]/count_words
    
    # Making list of comments present in test data
    test_data_objects = test_data["objects"]

    # Making an empty list to store the classes for each comment that our classifier gives for a comment
    result_label = []

    # Iterating through each comment in test data
    for each_data in test_data_objects:

        # cleaning comment removing punctuations and numbers and making each character to lower case
        each_data = each_data.translate(str.maketrans(' ', ' ', string.punctuation))
        each_data = ''.join(s for s in each_data if not s.isdigit())
        each_data = each_data.lower()

        # spliting comment to single(word) i.e. tokens
        words = each_data.split()

        # Initialaising probability of truthful and deceptive and taking in log to increase accuracy
        data_truthful = math.log10(p_truthful)
        data_deceptive = math.log10(p_deceptive)

        # Iterating through each token of comment
        for word in words:

            # If token in stop words we will continue i.e. we are not counting them in probability of comment being deceptive or truthful
            if word in stop_words:
                continue

            # If token in bag of truthful words we have multiply its probability with probability of comment being truthful 
            # but as we are taking log we will add both
            if word in bag_of_words_truthful:
                data_truthful += math.log10(bag_of_words_truthful[word])
            
            # If token in bag of deceptive words we have multiply its probability with probability of comment being deceptive 
            # but as we are taking log we will add both
            if word in bag_of_words_deceptive:
                data_deceptive += math.log10(bag_of_words_deceptive[word])
        
        # we are checking which probability is larger for a given comment and hence adding that label to result_label list
        if data_truthful < data_deceptive:
            result_label.append("deceptive")
        else:
            result_label.append("truthful")

    #returning the label list
    return result_label


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
