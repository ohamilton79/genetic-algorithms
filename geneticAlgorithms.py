#ohamilton79
#New Turing Omnibus Chapter 16 - Genetic algorithms
#20/02/2021
from random import randint, uniform

class Solution:
    def __init__(self, binaryVal = None):
        if binaryVal == None:
            #Get a random floating point number between -1 and 1
            self.floatVal = uniform(-1, 1)
            #Convert to binary representation (6 bits)
            self.binaryVal = self.floatToBinary(self.floatVal, 6)

        else:
            self.binaryVal = binaryVal
            self.floatVal = self.binaryToFloat(binaryVal)

        #Evaluate fitness of solution
        self.fitness = self.getFitness(self.floatVal)           

    #Define a function to evaluate the fitness of a solution
    def getFitness(self, x):
        return 8 * (x ** 2) + (8 * x) - 1

    #Convert a floating point number between 1 and -1 to its fixed-point binary representation
    def floatToBinary(self, aFloat, nOfBits):
        if aFloat < 0:
            negativeFlag = True
        else:
            negativeFlag = False

        binaryString = ""
            
        #Find the largest power of 2 that is less than the absolute value of the number
        largestPower = -1

        absoluteFloat = abs(aFloat)

        while len(binaryString) < nOfBits - 1:
            #Add a 0 if the place value is greater than the remaining number
            if (2**largestPower) > absoluteFloat:
                binaryString = binaryString + "0"

            #Add a one if the place value is less than (or equal to) the remaining number
            else:
                binaryString = binaryString + "1"
                #Get new number
                absoluteFloat -= (2**largestPower)

            #Analyse next place value
            largestPower -= 1

        #If the floating point number is negative, make the first bit a 1. Otherwise make it a 0
        if negativeFlag:
            binaryString = "1" + binaryString

        else:
            binaryString = "0" + binaryString

        return binaryString

    #Convert a fixed-point binary number in the sign-and-magnitude format to its floating point denary representation
    def binaryToFloat(self, binaryNum):
        #Get the sign of the number
        if binaryNum[0] == "1":
            sign = -1

        else:
            sign = 1

        floatNum = 0

        #Get the values of the remaining bits
        placePower = -1

        for i in range(1, len(binaryNum)):
            if binaryNum[i] == "1":
                floatNum += (2 ** placePower)

            placePower -= 1

        return sign * floatNum

#Cross 2 'chromosomes' by combining each half
def crossSols(firstSol, secondSol):
    firstBinarySol = firstSol.binaryVal
    secondBinarySol = secondSol.binaryVal
    
    binarySols = [firstBinarySol, secondBinarySol]
    #Choose a random index, indicating which chromosome contributes the first half of its alleles
    randIndex = randint(0, 1)

    firstHalf = binarySols[randIndex][0:len(firstBinarySol) // 2]
    secondHalf = binarySols[abs(randIndex - 1)][len(secondBinarySol) // 2:]

    crossedBinarySol = firstHalf + secondHalf

    #Create new solution to return
    crossedSol = Solution(crossedBinarySol)

    return crossedSol

#Mutate the solution by randomly flipping one of its bits
def mutate(sol):
    binarySol = sol.binaryVal
    #Get the index of a random bit to flip
    bitIndex = randint(0, len(binarySol) - 1)

    #Change a 0 to a 1
    if binarySol[bitIndex] == "0":
        binarySol = binarySol[:bitIndex] + "1" + binarySol[bitIndex+1:]

    #Change a 1 to a 0
    else:
        binarySol = binarySol[:bitIndex] + "0" + binarySol[bitIndex+1:]

    #Return the mutated 'chromosome' as an object
    mutatedSolution = Solution(binarySol)
    return mutatedSolution

#Sort Solution objects by fitnesses using a merge sort implementation
def sortByFitness(population):
    #If the size of the population is 1, it is sorted
    if len(population) > 1:
        #Recursively sort each half of the population
        mid = len(population) // 2
        leftHalf = population[0:mid]
        rightHalf = population[mid:]

        sortByFitness(leftHalf)
        sortByFitness(rightHalf)

        #Counter variables
        leftPointer = 0
        rightPointer = 0
        newListPointer = 0

        while leftPointer < len(leftHalf) and rightPointer < len(rightHalf):
            #If the left item's fitness is less than the right item's
            if leftHalf[leftPointer].fitness < rightHalf[rightPointer].fitness:
                #Insert the left item into the sorted list
                population[newListPointer] = leftHalf[leftPointer]
                #Increment left pointer
                leftPointer += 1

            #If the right item's fitness is less than the left item's
            else:
                #Insert the right item into the sorted list
                population[newListPointer] = rightHalf[rightPointer]
                #Increment right pointer
                rightPointer += 1

            #Get ready for inserting item into next list index
            newListPointer += 1

        #Insert any remaining items from the left and right lists
        while leftPointer < len(leftHalf):
            population[newListPointer] = leftHalf[leftPointer]
            #Increment pointers
            leftPointer += 1
            newListPointer += 1

        while rightPointer < len(rightHalf):
            population[newListPointer] = rightHalf[rightPointer]
            #Increment pointers
            rightPointer += 1
            newListPointer += 1

#Carry out a population cycle
def cycle(population, crossoverImprovement, mutationImprovement):
    #Store original population size, which is maintained
    n = len(population)
    #Sort each of the solutions by their fitness (merge sort)
    sortByFitness(population)

    #Breed the top 6 solutions in 3 pairs
    newSols = []
    newSols.append(crossSols(population[0], population[1]))
    newSols.append(crossSols(population[2], population[3]))
    newSols.append(crossSols(population[4], population[5]))

    #Check if any of the crossed solutions are improvmenets over their parents
    parent1Index = 0
    parent2Index = 1

    for sol in newSols:
        if sol.fitness < population[parent1Index].fitness or sol.fitness < population[parent2Index].fitness:
            crossoverImprovement += 1

        parent1Index += 2
        parent2Index += 2

    #Mutate one of the top 6 solutions and one of the bottom four
    solToMutate = population[randint(0, 5)]
    newSols.append(mutate(solToMutate))

    #Update mutation counter
    if newSols[3].fitness < solToMutate.fitness:
        mutationImprovement += 1
        
    solToMutate = population[randint(len(population) - 5, len(population) - 1)]
    newSols.append(mutate(population[randint(len(population) - 5, len(population) - 1)]))
    #Update mutation counter
    if newSols[4].fitness < solToMutate.fitness:
        mutationImprovement += 1

    #Insert each of the new solutions into the correct position in the population list, sorted by fitness
    for newSol in newSols:
        inserted = False
        i = len(population) - 1
        while not inserted and i >= 0:
            if population[i].fitness > newSol.fitness:
                population.insert(i, newSol)
                #Set flag to indicate new solution has been inserted
                inserted = True

            #Decrement counter to examine next population item
            i -= 1

    #Retain the n solutions with the lowest fitness
    population = population[0:n]
    return population, crossoverImprovement, mutationImprovement

#START OF PROGRAM EXECUTION

#Define initial values
population = [Solution() for x in range(10)]    #Maintain a population of 10 solutions
crossoverImprovement = 0
mutationImprovement = 0

print("Fitnesses: {}".format([solution.fitness for solution in population]))

#Perform 10 population cycles
for x in range(10):
    population, crossoverImprovement, mutationImprovement = cycle(population, crossoverImprovement, mutationImprovement)
    print("Fitnesses: {}".format([solution.fitness for solution in population]))
    print("Crossover improvement percentage: {}%".format((crossoverImprovement / 30) * 100))   #Divide by 300 as 3 crossovers performed in a population cycle
    print("Mutation improvement percentage: {}%".format((mutationImprovement / 20) * 100))     #Divide by 200 as 2 mutations performed in a population cycle



    
    
