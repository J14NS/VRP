#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-06-08 21:45:45
# @Author  : Jian Shen (J.Shen@soton.ac.uk)
# @Link    : N/A
# @Version : $Id$


import pandas as pd
import numpy
import random
import copy
#Read data from csv; Set input variables
csv_data = pd.read_csv('I20.csv')  
location_city = csv_data.iloc[:, 1:3]
location_cities = location_city.values
num_city = len(csv_data)
#Set parameters
#maxGen = 5 * num_city + 25
maxGen = 1
popSize = 20
crossoverP = 0.9
mutationP = 0.9

gbest = None

# define function to calculate matrix 

def calculateDis(location, num):
	dis = numpy.zeros(shape=(num,num))
	for i in range(0,num):
		for j in range(0,num):
			dis[i,j] = numpy.sqrt(numpy.square(location[i,0] - location[j,0]) + numpy.square(location[i,1]-location[j,1]))
	return dis


DisMa = calculateDis(location_cities, num_city)
print("Until now is good! God bless you...")

# Sample Generate


def SampleGenerate(popSize, num):
	# Define necessary parameters
	n = num - 2
	pop = numpy.zeros(shape = (popSize, num))
	threshold = num/2
	for j in range(0, popSize):
		cdd = numpy.random.permutation(n) + 2
		even = cdd[numpy.array(cdd % 2 ==0,dtype='bool')]
		odd = cdd[numpy.array(cdd % 2 ==1,dtype='bool')]
		extra = 0

		if len(even) % 2 == 1:
			extra = 1
			tempindex = numpy.array(numpy.argwhere(even >= threshold))
			extraeven = even[tempindex[0]]
			even = numpy.delete(even, tempindex[0])
		i = 1
		NodeCell = []
		# Check for initial combination
		while len(numpy.argwhere(even >= threshold)) > 0:
			tempindex = numpy.array(numpy.argwhere(even >= threshold))
			temp = even[tempindex[0]]
			even = numpy.delete(even, tempindex[0])
			if len(even) >0:
				temp = numpy.append(temp, even[0])
				even = numpy.delete(even, 0)
			if temp[len(temp)-1] >= threshold:
				temp = numpy.append(temp, even[0])
				even = numpy.delete(even, 0)
			temp = temp.tolist()
			if i == 0:
				NodeCell = numpy.empty((1,), dtype = object)
				NodeCell[0] = temp
			else:
				NodeCell = numpy.append(NodeCell, numpy.empty((1,), dtype = object))
				NodeCell[len(NodeCell)-1] = temp
			i = i + 1

		while len(even) > 0:
			NodeCell = numpy.append(NodeCell, numpy.empty((1,), dtype = object))
			temp = even[0]
			temp = temp.tolist()
			NodeCell[len(NodeCell)-1] = temp
			even = numpy.delete(even, 0)

		while len(numpy.argwhere(odd < threshold)) > 0:
			tempindex = numpy.array(numpy.argwhere(odd < threshold))
			temp = odd[tempindex[0]]
			odd = numpy.delete(odd, tempindex[0])
			if len(odd) > 0:
				temp = numpy.append(temp, odd[0])
				odd = numpy.delete(odd, 0)

			if temp[len(temp)-1] < threshold:
				temp = numpy.append(temp, odd[0])
				odd = numpy.delete(odd, 0)
			temp = temp.tolist()
			NodeCell = numpy.append(NodeCell, numpy.empty((1,), dtype = object))
			NodeCell[len(NodeCell)-1] = temp

		while len(odd) > 0:
			NodeCell = numpy.append(NodeCell, numpy.empty((1,), dtype = object))
			temp = odd[0]
			temp = temp.tolist()
			NodeCell[len(NodeCell)-1] = temp
			odd = numpy.delete(odd, 0)	
		
		len_NodeCell = len(NodeCell)
		ord_NodeCell = numpy.random.permutation(len_NodeCell)
		NodeList = []
		for i in range(0, len_NodeCell):
			temp = numpy.asarray(NodeCell[ord_NodeCell[i]])
			NodeList = numpy.append(NodeList, temp)

		if extra == 1:
			NodeList = numpy.append(NodeList, extraeven)
		NodeList = numpy.append(NodeList, num)
		NodeList = numpy.append(1, NodeList)
		pop[j,:] = NodeList
		pop = pop.astype(int)

	return(pop)
pop = SampleGenerate(popSize,num_city)

def fitness(Dis, pop, gen):
	popSize = numpy.shape(pop)[0]
	col = numpy.shape(pop)[1]
	sumDistance = numpy.zeros(shape = (popSize, 1))
	subDistance = numpy.zeros(shape = (popSize, col-1))
	for i in range(0, popSize):
		for j in range(0, col-1):
			subDistance[i,j] = Dis[pop[i,j]-1, pop[i,j+1]-1]
			sumDistance[i] = sumDistance[i] + subDistance[i,j]
	L = numpy.max(Dis)
	maxDis = numpy.max(subDistance, axis = 1)
	minDis = numpy.min(subDistance, axis = 1)
	Delta = maxDis - minDis
	Delta = Delta.reshape(Delta.shape[0], 1)
	FunctionalValuePart = 0

	if gen <= 10:
		maxDisbench = numpy.max(subDistance, axis = 1)
		minDisbench = numpy.min(subDistance, axis = 1)
		Deltabench = maxDisbench - minDisbench
		Deltabench = Deltabench.reshape(Deltabench.shape[0], 1)
		FunctionalValuePart = sumDistance + Deltabench * (col-2) * L

	if gen <= 5 * col and gen > 10:
		BenchSize = gen // 10 + col // 2
		startbench = random.randint(0, col-BenchSize+1)
		endbench = startbench + BenchSize - 1
		maxDisbench = numpy.max(subDistance[:, startbench:endbench], axis = 1)
		minDisbench = numpy.min(subDistance[:, startbench:endbench], axis = 1)
		Deltabench = maxDisbench - minDisbench
		Deltabench = Deltabench.reshape(Deltabench.shape[0], 1)
		FunctionalValuePart = sumDistance + Deltabench * (col-2) * L

	if gen > 5 * col:
		FunctionalValuePart = sumDistance + Delta * (col-2) * L

	FunctionalValue = sumDistance + Delta * (col-2) * L

	return subDistance, sumDistance, Delta, FunctionalValuePart, FunctionalValue



def crossover(parent1Path, parent2Path, crossoverP):
	subparent1Path = copy.deepcopy(parent1Path[1:len(parent1Path)-1])
	subparent2Path = copy.deepcopy(parent2Path[1:len(parent2Path)-1])	

	n = len(subparent1Path)
	threshold = n/2 + 1
	cross_rand = random.uniform(0, 1)
	childPath = numpy.zeros(shape = (n)) 
	parent1Part = 0
	p1 = 0
	if crossoverP >= cross_rand:
		setSize = n//2
		offset = random.randint(1, setSize)
		endset = setSize + offset - 1
		childPath[offset-1:endset] = copy.deepcopy(subparent1Path[offset-1:endset])
		account = endset
		for i in range(0, n):
			if any(childPath == subparent2Path[i]):
				subparent2Path[i] = 0
		subparent2Path = [x for x in subparent2Path if x !=0]
		parent1Part = numpy.zeros(shape = (n-setSize))
		parent1Part[0:offset-1] = copy.deepcopy(subparent1Path[0:offset-1])
		parent1Part[offset-1:len(parent1Part)] = copy.deepcopy(subparent1Path[endset:len(subparent1Path)])
		subparent2Path = numpy.asarray(subparent2Path)
		p1 = subparent2Path[numpy.array(numpy.argwhere((subparent2Path % 2 == 0) & (subparent2Path >= threshold)))]
		p1index = numpy.array(numpy.argwhere((parent1Part % 2 == 0) & (parent1Part >= threshold)))
		for i in range(0, len(p1)):
			parent1Part[p1index[i]] = p1[i]
		p2 = subparent2Path[numpy.array(numpy.argwhere((subparent2Path % 2 == 0) & (subparent2Path < threshold)))]
		p2index = numpy.array(numpy.argwhere((parent1Part % 2 == 0) & (parent1Part < threshold)))
		for i in range(0, len(p2)):
			parent1Part[p2index[i]] = p2[i]
		p3 = subparent2Path[numpy.array(numpy.argwhere((subparent2Path % 2 == 1) & (subparent2Path >= threshold)))]
		p3index = numpy.array(numpy.argwhere((parent1Part % 2 == 1) & (parent1Part >= threshold)))
		for i in range(0, len(p3)):
			parent1Part[p3index[i]] = p3[i]
		p4 = subparent2Path[numpy.array(numpy.argwhere((subparent2Path % 2 == 1) & (subparent2Path < threshold)))]
		p4index = numpy.array(numpy.argwhere((parent1Part % 2 == 1) & (parent1Part < threshold)))
		for i in range(0, len(p4)):
			parent1Part[p4index[i]] = p4[i]

		childPath[0:offset-1] = parent1Part[0:offset-1]
		childPath[endset:len(childPath)] = parent1Part[offset-1:len(parent1Part)]
	else:
		childPath = parent1Path
	childPath = numpy.append(childPath, n+2)
	childPath = numpy.append(1, childPath)
	return(childPath)

def mutate(path, mutationP):
	subPath = copy.deepcopy(path[1:len(path)-1])
	n = len(subPath)
	mutate_rand = random.uniform(0, 1)
	threshold = n/2 + 1
	

	return subPath


offspring = numpy.zeros(shape=(popSize, num_city))

minPathes = numpy.zeros(shape=(maxGen ,1))
minDistance = numpy.zeros(shape=(maxGen ,1))
minFvPath = numpy.zeros(shape=(maxGen, num_city))
minFv = numpy.zeros(shape=(maxGen ,1))
minDelta = numpy.zeros(shape=(maxGen, 1))

# To Obtain Each Generations Iteratively

for gen in range(0, maxGen):
	subDistance, sumDistance, Delta, FunctionValuePart, FunctionValue = fitness(DisMa, pop, gen)
	tournamentSize = 4
	for k in range(1, popSize):
		tourPopDistance = numpy.zeros(shape = (tournamentSize, 1))
		for i in range(0, tournamentSize):
			randomRow = random.randint(0, popSize-1)
			tourPopDistance[i] = FunctionValuePart[randomRow, 0]
		parent1 = numpy.min(tourPopDistance)
		parent1X = numpy.array(numpy.argwhere(FunctionValuePart == parent1))
		parent1_Path = pop[parent1X[0,0],:]
		for i in range(0, tournamentSize):
			randomRow = random.randint(0, popSize-1)
			tourPopDistance[i] = FunctionValuePart[randomRow, 0]
		parent2 = numpy.min(tourPopDistance)
		parent2X = numpy.array(numpy.argwhere(FunctionValuePart == parent2))
		parent2_Path = pop[parent2X[0,0],:]		
		subPath = crossover(parent1_Path,parent2_Path,crossoverP)
		subPath = mutate(subPath, mutationP)



























