###################################
# CS B551 Spring 2021, Assignment #3
#
# Your names and user ids: Himanshu Himanshu(hhimansh), Varsha Ravi Varma(varavi), Aman Chaudhary(amanchau)
#
# (Based on skeleton code by D. Crandall)
#
# Reference for mcmc implementation: https://github.com/ajcse1/Part-of-Speech-Tagger/blob/master/pos_solver.py 
# Reference for Viterbi Implemenattion: Professor David Crandall implementation from class exercise 

from os import W_OK
import random
import math
from numpy.lib.function_base import copy


from numpy.lib.scimath import log10
from numpy.random.mtrand import sample


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):

        # Depending on each algorithm deciding what have to do to calculate posterior probability
        if model == "Simple":

            # taking post prob as  1 as we have to do multiplication
            post_prob = 1

            # Iterating through each label and word
            for i in range(len(label)):

                # finding tag and word at ith index
                tag = label[i]
                word = sentence[i]

                # checking if word is in word emission probability if it is then checking probability of tag assigned to it given word
                if word in self.word_emit_prob and self.word_emit_prob[word][tag] != 0:
                    post_prob *= self.word_emit_prob[word][tag] * self.tag_prob[tag]
                else:

                    #if word not exist or probability of tag given word is zero then taking it as 0.000000001
                    post_prob *= 0.000000001  * self.tag_prob[tag]
            
            # if posterior comes out to be 0 so setting it to 0.000000001
            if post_prob == 0:
                post_prob = 0.000000001

            # returning log of posterior
            return math.log10(post_prob)
        elif model == "HMM":

            # taking post prob as  1 as we have to do multiplication
            post_prob = 1

            # Iterating through each label and word
            for i in range(len(label)):

                # finding tag and word at ith index
                tag = label[i]
                word = sentence[i]

                # checking if word is in word emission probability if it is then checking probability of tag assigned to it given word
                if word in self.word_emit_prob and self.word_emit_prob[word][tag] != 0:
                    post_prob *= self.word_emit_prob[word][tag]
                else:
                    #if word not exist or probability of tag given word is zero then taking it as 0.000000001
                    post_prob *= 0.000000001
            
            #multiplying probability of tag i
            post_prob *= self.tag_prob[label[0]]

            # Multiplying each transition probability
            for i in range(1, len(label)):
                if self.trans_tag_prob[label[i-1]][label[i]] != 0:
                    post_prob *= self.trans_tag_prob[label[i-1]][label[i]]
                else:
                    post_prob *= 0.000000001
            
            # if posterior comes out to be 0 so setting it to 0.000000001
            if post_prob == 0:
                post_prob = 0.000000001

            # returning log of posterior
            return math.log10(post_prob)
        elif model == "Complex":

            # taking post prob as  1 as we have to do multiplication
            post_prob = 1

            # finding lenth of swntence
            N = len(sentence)

            # iterating through each word and tag
            for i in range(N):

                # setting emit probability as 0.000000001
                emit_prob = 0.000000001

                # if word exist in word emit probability and its value is not zero then setting it
                if sentence[i] in self.word_emit_prob and self.word_emit_prob[sentence[i]][label[i]] != 0:
                    emit_prob = self.word_emit_prob[sentence[i]][label[i]]
                
                # setting transition probability from current state to next state and initially setting it as 0.000000001 
                trans_prob1 = 0.000000001
                if i != N - 1:
                    trans_prob1 = self.trans_tag_prob[label[i]][label[i+1]]

                # setting transition probability from last state to current state and initially setting it as 0.000000001
                trans_prob2 = 0.000000001
                if i != 0:
                    trans_prob2 = self.trans_tag_prob[label[i-1]][label[i]]
                
                #if index is 0 we have to multiply transition probability from current state to next state to emission prob 
                # and tag prob of curr tag
                if i == 0:
                    post_prob *= trans_prob1 * emit_prob * self.tag_prob[label[i]]
                
                #if index is N-1 we have to multiply transition probability from last state to current state to emission prob 
                # and tag prob of last tag
                elif i == N - 1:
                    post_prob *= trans_prob2 * emit_prob * self.tag_prob[label[i-1]]

                #otherwise we have to multiply transition probability from current state to next state to emission prob, 
                # tag prob of last tag and transition probability from last state to current state
                else:
                    post_prob *= trans_prob1 * trans_prob2 * emit_prob * self.tag_prob[label[i-1]]
            
             # if posterior comes out to be 0 so setting it to 0.000000001
            if post_prob == 0:
                post_prob = 0.000000001

            # returning log of posterior
            return math.log10(post_prob)
        else:
            print("Unknown algo!")

    # Do the training!
    # Calculating all the probabilities that would be used in this in the training function wheterher its tag probability,
    # tag list, transition probability, initial probability and emission probability and it done from ata of training file
    def train(self, data):

        # taking all the the probabilities dictionary and setting it to empty and taking all as instance variable so it can be used furthur
        # It will be a dictionary with tag as key and probability of its occurance as key
        self.tag_prob= {}

        # It will be a nested dictionary key as tag and value as dictionary of tags as key and there transition probaility as value
        self.trans_tag_prob = {}
        self.tag_list = []

        # It will be a nested dictionary word as key and value as dictionary of tags as key and there probaility to occur for a given 
        # word as value
        self.word_emit_prob = {}
        
         # It will be a dictionary with tag as key and probability of its occurance first in sentence as key
        self.init_prob = {}
        
        # setting N as length of data
        N = len(data)

        # Iterating through each sentence and its tag list in data
        for i in range(N):
            tags = data[i][1]
            words = data[i][0]

            # setting initial occurance of a tag, if its already there then increasing it else initialising it
            if tags[0] in self.init_prob:
                self.init_prob[tags[0]] += 1
            else:
                self.init_prob[tags[0]] = 1
            
            # Iterating through each tag to set transition of each tag in sentence
            for j in range(len(tags)-1):

                # find current and next tag
                curr_tag = tags[j]
                next_tag = tags[j+1]

                # if current tag is in transition dictionary
                if curr_tag in self.trans_tag_prob:

                    # checking if next tag is in transition dictionary of current tag if it  is increase count by 1 
                    # otherwise initialise it to 1
                    if next_tag in self.trans_tag_prob[curr_tag]:
                        self.trans_tag_prob[curr_tag][next_tag] += 1
                    else:
                        self.trans_tag_prob[curr_tag][next_tag] = 1
                else:
                    # if current tag is in not transition dictionary, initialising its transition dictionary and setting value 
                    # of next tag in it as 1
                    self.trans_tag_prob[curr_tag] = {}
                    self.trans_tag_prob[curr_tag][next_tag] = 1

            # Iterating through each tag to setting its occurance
            for tag in tags:

                # if tag already exist increase it is occurance by 1 otherwise initialising its occurance by 1
                if tag in self.tag_prob:
                    self.tag_prob[tag] += 1
                else:
                    self.tag_prob[tag] = 1

            # Iteratating through each word and setting count of tag for each word 
            for j in range(len(words)):

                # if word already exist word emission dictionary
                if words[j] in self.word_emit_prob:

                    # checking if tag exist for word in emission dictionary if yes ibcreasing its count by 1 else initialising it to 1
                    if tags[j] in self.word_emit_prob[words[j]]:
                        self.word_emit_prob[words[j]][tags[j]] += 1
                    else:
                        self.word_emit_prob[words[j]][tags[j]] = 1
                else:
                    # Otherwise initialising dictionary word and setting occurance of tag to 1 in that dictioanry
                    self.word_emit_prob[words[j]] = {}
                    self.word_emit_prob[words[j]][tags[j]] = 1
        
        # finding tag list by finding keys
        self.tag_list = self.tag_prob.keys()

        # finding total count of tags 
        count_of_tag = sum(self.tag_prob.values())

        # Iterating through each tag key in dictionary to set it to probability value dividing it by total count
        for tag in self.tag_prob:
            self.tag_prob[tag] = self.tag_prob[tag] / count_of_tag
        
        # Iterating through each tag initialising probability dictionary and setting to corresponding probability value 
        # by dividing it by number of sentence
        for tag in self.init_prob:
            self.init_prob[tag] = self.init_prob[tag] / N

        # If any tag from tag list doesn't exist in inittag probability setting it to 0
        for tag in self.tag_list:
            if tag not in self.init_prob:
                self.init_prob[tag] = 0
        
        # Changing count of transition to transition probability for each tag from each tag by iterating
        for tag in self.trans_tag_prob:

            # finding total count of transition for particular tag to other tag
            sum_of_count = sum(self.trans_tag_prob[tag].values())

            # converting count to trans probability bt diving by total count
            for key in self.trans_tag_prob[tag]:
                self.trans_tag_prob[tag][key] = self.trans_tag_prob[tag][key] / sum_of_count
            
            # Iterating through list of tags if any tag doesn't exist setiing its probability as 0
            for key in self.tag_list:
                if key not in self.trans_tag_prob[tag]:
                    self.trans_tag_prob[tag][key] = 0
       
       # Changing word emit probability dictionary which is probability of tag if a word is given from its count to probability
        for word in self.word_emit_prob:

            # finding total occurance of word in data
            total_count_word = sum(self.word_emit_prob[word].values())

            # convering count of tag to probability by dividing by total count 
            for tag in self.word_emit_prob[word]:
                self.word_emit_prob[word][tag] = self.word_emit_prob[word][tag] / total_count_word

            # Iterating through each tag in tag list
            for key in self.tag_list:

                # if a tag doesn't exist for word setting its probability to 0
                if key not in self.word_emit_prob[word]:
                    self.word_emit_prob[word][key] = 0 
    
    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #This method is for simplified Bayesian model we are just passing sentence into it
    def simplified(self, sentence):

        # Taking an empty predicted tag list
        predict_tag = []

        # Iterating through each word in sentence
        for word in sentence:

            # If that word doesn't exist in word_emit_prob dictionary meaning 
            # it was not in training data appending noun for it in predicted tag list and continue to next word
            if word not in self.word_emit_prob:
                predict_tag.append('noun')
                continue

            #If the word exist exit 
            # we will initially take max prob tag as noun and max prob as 0
            max_prob_tag = 'noun'
            max_prob = 0

            # iterating through each tag in word_emit_prob dictionary for that word
            for tag in self.word_emit_prob[word]:
                
                # find the probability of occurrance of that tag my multiplying emit probabaility of that 
                # tag for that word and occurance probability of tag 
                prob = self.word_emit_prob[word][tag] * self.tag_prob[tag] 

                # if probability is greater than max probability then setting tag as max probable tag 
                # and max probability as current probability
                if  prob > max_prob:
                    max_prob_tag =  tag
                    max_prob = prob
            # appending the max probable tag predicted tag lsit for that word
            predict_tag.append(max_prob_tag)

        # returning predicted tag list
        return predict_tag

    # This method is for HMM Viterbi algorithm, 
    # reference for this implementation is taken from Professor David Carndall Implementation of Viterbi in Class exercise
    def hmm_viterbi(self, sentence):

        # finding no of words in sentence
        N = len(sentence)

        # Initialising empty V table to mantain what is highest probability to reach that particular state from previous state
        V_table = {}

        # Initialising empty which table to mantain from which previous state we can reach that particular state with highest probability
        which_table = {}

        # initialisih N length matrix for each tag
        for tag in self.tag_list:
            V_table[tag] = [0] * N
            which_table[tag] = [0] * N

        # Finding V_table probability for index word at index 0 for each tag
        for tag in self.tag_list:

            # setting emit_prob as 0.000000001
            emit_prob = 0.000000001

            # checking if word at index 0 exist in word_emit_prob if yes then finding its emit probabilty from dictionary
            if sentence[0] in self.word_emit_prob:
                    emit_prob = self.word_emit_prob[sentence[0]][tag]
            
            # multiplying emit_probability with initial probability of tag and setting it as V_table of tag for index 0
            V_table[tag][0] = self.init_prob[tag] * emit_prob
        
        # Iterating through other words in sentence other than at index 0
        for i in range(1, N):

            # finding word and index i
            word = sentence[i]

            # Iterating through tag in taglist to find best possible state and probability to reach that state
            for tag in self.tag_list:

                # Finding best tag from previous state and max probability by which we can reach a particular tag for word at index i 
                # by multiplying probability of each tag from previous state and multiplying it by transition probabilty and finding max of it
                (which_table[tag][i], V_table[tag][i]) =  max( [ (s0, V_table[s0][i-1] * self.trans_tag_prob[s0][tag]) for s0 in self.tag_list ], key=lambda l:l[1] )
                
                # setting emission probability as 0.000000001
                emit_prob = 0.000000001

                # If word exist in word_emit_prob dictionary then finding emit_prob from dictionary
                if word in self.word_emit_prob:
                    emit_prob = self.word_emit_prob[word][tag]
                
                # setting probability in v_table for that tag and index by multiplying best probability by emission probabilty
                V_table[tag][i] = V_table[tag][i] * emit_prob

        # Initialising a predicted tag list of size N with all value as noun
        predicted_tag = [ "noun" ] * N
        prob = -1

        # Iterating through every key in V_table and finding value of N-1 index if its greater than prob initially set as -1 
        # setting prob to this this V_table value as predeicted tag of N-1 index as key
        for key in V_table:
            if V_table[key][N - 1] > prob:
                prob  = V_table[key][N - 1]
                predicted_tag[N - 1] = key

        # Iterating through each predicted tag index in reverse order starting from last index -1 and topping till reach 0
        for i in range(N-2, -1, -1):

            # finding preicted tag for i index using which table i.e through backtracking
            predicted_tag[i] = which_table[predicted_tag[i+1]][i+1]

        # returning predicted_tag list
        return predicted_tag

    # This is implemenetation for sample generator and finding its probability for mcmc algorithm
    # Implementation of this whole method is taken from github repo: https://github.com/ajcse1/Part-of-Speech-Tagger/blob/master/pos_solver.py
    def generate_samples(self, sentence, sample):

        # finding length of senetence
        N = len(sentence)
        tags = list(self.tag_list)

        # Iterating through each word in sentence
        for i in range(N):

            # finding word at index i
            word = sentence[i]

            # Making an empty probability list
            prob = []

            # setting tag1 which is tag of previous state as empty
            tag_prev = " "

            # if index is greater than 0 then setting tag1 from previous state 
            if i > 0:
                tag_prev = sample[i - 1]

            # setting tag2 which is tag to next state as empty
            tag_next = " "

            # if index is less than N-1 then setting tag2 from next state
            if i < N - 1:
                tag_next = sample[i + 1]

            #Iterating through each tag in the list
            for j in range(len(tags)):

                # taking tag at index j
                tag = tags[j]

                #setting emit_prob as 0.000000001
                emit_prob = 0.000000001

                # if word exist in emit prob dictionary finding it emit prob from there 
                if word in self.word_emit_prob:
                    emit_prob = self.word_emit_prob[word][tag]

                # Finding transition probability from current state to next if exist otherwise setting it as 0.000000001
                trans_prob1 = 0.000000001
                if tag_next in self.trans_tag_prob[tag]:
                    trans_prob1 = self.trans_tag_prob[tag][tag_next]
                
                # Finding transition probability from previous state to current if exist otherwise setting it as 0.000000001
                trans_prob2 = 0.000000001
                if tag_prev in self.trans_tag_prob:
                    trans_prob2 = self.trans_tag_prob[tag_prev][tag]

                # appending ifferent multiplication prob depending on different location major difference is transition probability only
                if i == 0:
                    prob.append(trans_prob1 * emit_prob * self.tag_prob[tag])
                elif i == N - 1:
                    prob.append(trans_prob2 * emit_prob * self.tag_prob[tag_prev])
                else:
                    prob.append(trans_prob1 * trans_prob2 * emit_prob * self.tag_prob[tag_prev])

            # finding sum of sum of all probabilities in the list
            sum_of_prob = sum(prob)

            # If sum of all probabilities is not zero divide each probablity by sum of probability to normalise
            if sum_of_prob!= 0:
                prob = [value / sum_of_prob for value in prob]

            # Taking a random float
            random_number = random.random()

            # for findinding cuummulative sum
            p_sum = 0

            #iterating through each probability found till now
            for k in range(len(prob)):
                
                # adding each prob to sum
                p_sum += prob[k]

                # if prob sum become greater than random number we set sample [i] as tag[k]
                if random_number < p_sum:
                    sample[i] = tags[k]
                    break
    
    # Main method for mcmc algorithm implementation
    def complex_mcmc(self, sentence):

        # Taking number of words
        N = len(sentence)

        # initialising predicted tag array of size N
        sample = ["noun"] * N

        # Running generate sample for 2000 samples
        for i in range(2000):
            self.generate_samples(sentence, sample)
    
        #returning the last generated sample
        return sample



    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")

