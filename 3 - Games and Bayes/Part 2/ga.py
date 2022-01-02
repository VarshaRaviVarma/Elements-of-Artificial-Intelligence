import math
from AnimatedQuintris import *
from SimpleQuintris import *
from QuintrisGame import *
from kbinput import *
import time, sys
import random
import copy
from computergame import ComputerPlayer


class Genetic:

    #Function to generate random integers
    def randomInt(self, min, max):
        return math.floor(random.randint() * (max - min) + min)

    #Function to generate random samples
    def candidate_generation(self):
        sample = {
            'heightWeight': random.random() - 0.5,
            'linesWeight': random.random() - 0.5,
            'holesWeight': random.random() - 0.5,
            'bumpinessWeight': random.random() - 0.5,
            'wellWeight' : random.random() - 0.5
        }
        #Calling the normalize function on sample
        self.normalize(sample)
        return sample

    #Function to compute the fitness
    def compute_fitness(self, samples, numberOfGames):
        for i in range(len(samples)):
            sample = samples[i]
            #Initizalizing total score to 0
            totalScore = 0

            for j in range(numberOfGames):
                #Calling the ComputerPlayer by passing the heuristics
                quintris = ComputerPlayer(sample['heightWeight'], sample['bumpinessWeight'], sample['wellWeight'], sample['holesWeight'], sample['linesWeight'])
                try: 
                    #Generating a simple quintris
                    simple_quintris = SimpleQuintris()
                    #Starting the quintris game
                    simple_quintris.start_game(quintris)
                except:
                    #Appending the value obtained to the total scsore
                    totalScore += simple_quintris.state[1]
                    print("Finished! Game Over!")
                    #Printing the total score
                    print("Score= " + str(totalScore))

            #Assigning the fitness with the total score
            sample['fitness'] = totalScore

    #Function to sort the list of dictionaries depending on fitness
    def sort(self, samples):
        sorted_candidates = sorted(samples, key = lambda d : d['fitness'], reverse = True)
        return sorted_candidates

    #Selection of 10% of the population at random
    def pair_selection(self, samples, ways):
        indices = []
        for i in range(len(samples)):
            indices.append(i)

        #Initializing the 2 fittest candidates to None
        fittestCandidateIndex1 = None
        fittestCandidateIndex2 = None

        for i in range(ways):
            #Generating a random integer
            r_int = random.randint(0,len(indices)-1)
            print(r_int)
            #Popping off the random integer generated and storing it in selectedIndex
            selectedIndex = indices.pop(r_int)
            #Assigning the values to the fittest samples
            if (fittestCandidateIndex1 == None or selectedIndex < fittestCandidateIndex1):
                fittestCandidateIndex2 = fittestCandidateIndex1
                fittestCandidateIndex1 = selectedIndex
            #Performing conditional check to update sample 2
            elif(fittestCandidateIndex2 == None or selectedIndex < fittestCandidateIndex2):
                fittestCandidateIndex2 = selectedIndex

        return [samples[fittestCandidateIndex1], samples[fittestCandidateIndex2]]

    #Crossover by multiplying the fitness by different heuristics of both samples
    def crossOver(self, candidate1, candidate2):
        sample = {
            'heightWeight': candidate1['fitness']* candidate1['heightWeight'] + candidate2['fitness']* candidate2['heightWeight'],
            'linesWeight': candidate1['fitness'] * candidate1['linesWeight'] + candidate2['fitness'] * candidate2['linesWeight'],
            'holesWeight': candidate1['fitness'] * candidate1['holesWeight'] + candidate2['fitness'] * candidate2['holesWeight'],
            'bumpinessWeight': candidate1['fitness']* candidate1['bumpinessWeight'] + candidate2['fitness'] * candidate2['bumpinessWeight'],
            'wellWeight': candidate1['fitness'] * candidate1['wellWeight'] + candidate2['fitness'] * candidate2['wellWeight']
        }
        #Calling the normalize function on sample
        self.normalize(sample)
        return sample

    #Function to offspring_mutation by assigning 5% chance of mutation
    def offspring_mutation(self,sample):
        quantity = random.random() * 0.4 - 0.2
        random_int = random.randint(0, 5)
        #If random int generated is 0
        if (random_int == 0):
            sample['heightWeight'] += quantity
        #If random int generated is 1
        if (random_int == 1):
            sample['linesWeight'] += quantity
        #If random int generated is 2
        if (random_int == 2):
            sample['holesWeight'] += quantity
        #If random int generated is 3
        if (random_int == 3):
            sample['bumpinessWeight'] += quantity
        #If random int generated is 4
        if (random_int == 4):
            sample['wellWeight'] += quantity

    #Fucntion to normalize
    def normalize(self, sample):
        norm = math.sqrt(sample['heightWeight'] ** 2 + sample['linesWeight'] ** 2 + sample['holesWeight'] ** 2 + sample['bumpinessWeight'] ** 2 +  sample['wellWeight'] ** 2)
       
        #If value of norm is equal to 0 assign it to 1
        if (norm == 0):
            norm = 1

        #Dividing the heightWeight by the norm
        sample['heightWeight'] /= norm
        #Dividing the linesWeight by the norm
        sample['linesWeight'] /= norm
        #Dividing the holesWeight by the norm
        sample['holesWeight'] /= norm
        #Dividing the bumpinessWeight by the norm
        sample['bumpinessWeight'] /= norm
        #Dividing the wellWeight by the norm
        sample['wellWeight'] /= norm

    #Function to delete the weakest 30% offsprings and replacing them with the newly generated offsprings. 
    def delete_replacement(self, samples, newCandidates):
        for i in range(len(newCandidates)):
            #Appending the ith index from the newCandidate to samples
            samples.append(newCandidates[i])
        #Calling the sort function on the samples
        self.sort(samples)   

    #Main function main_genetic
    def main_genetic(self):

        #Creating a dictionary with config population and number of rounds
        config = {'ppn': 10, 'rounds': 5}

        #Intializing an empty samples list
        samples = []
        for i in range(config['ppn']):
            #Appending the randomly generated candidates to the samples list
            samples.append(self.candidate_generation())

        #Computing the fitness of the samples.
        self.compute_fitness(samples, config['rounds'])
        #Calling the sort function on the samples list
        samples = self.sort(samples)

        count = 0

        while(count<2):
            #Initializing an empty list
            newCandidates = []
            #Iterating 30 times
            for i in range(30):
                #Calling the select pair function to select the pair
                pair = self.pair_selection(samples, 10)
                #Performing crossover on the 2 samples
                sample = self.crossOver(pair[0], pair[1])

                #Condition to perform mutation on the offsprings
                if(random.random()<0.05):
                    self.offspring_mutation(sample)
                
                #Calling the normalize function on the sample
                self.normalize(sample)
                #Appending the sample to the newCandidate
                newCandidates.append(sample)

            #Computing the fitness of the new sample 
            self.compute_fitness(newCandidates, config['rounds'])
            #Calling the delete and replace on the new samples
            self.delete_replacement(samples, newCandidates)

            totalFitness = 0

            for i in range(len(samples)):
                totalFitness += samples[i]['fitness']
            
            #Increasing the count to 1
            count += 1
            max_fit = max(samples, key=lambda x:x['fitness'])
            print(samples)
            print()
            print(max_fit)

#Making an object of the Genetic class     
genetic = Genetic()
#Calling the main_genetic function of the Genetic class
genetic.main_genetic()