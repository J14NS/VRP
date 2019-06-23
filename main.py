#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-06-08 21:45:45
# @Author  : Jian Shen (J.Shen@soton.ac.uk)
# @Link    : N/A
# @Version : $Id$


import pandas as pd
import numpy


#Read data from csv; Set input variables
csv_data = pd.read_csv('I20.csv')  
location_city = csv_data.iloc[:, 1:3]
location_cities = location_city.values
num_city = len(csv_data)
#Set parameters
maxGen = 5 * num_city + 25
popSize = 2
crossoverP = 0.1
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
	FunctionalValuePart = 0

	if gen <= 10:
		maxDisbench = numpy.max(subDistance, axis = 1)
		minDisbench = numpy.min(subDistance, axis = 1)
		Deltabench = maxDisbench - minDisbench
		FunctionalValuePart = sumDistance + Deltabench * (col-2) * L

	if gen <= 5 * col and gen > 10:
		BenchSize = gen // 10 + col // 2
		startbench = random.randint(0, col-benchSize+1)
		endbench = startbench + BenchSize - 1
		maxDisbench = numpy.max(subDistance[:, startbench:endbench], axis = 1)
		minDisbench = numpy.min(subDistance[:, startbench:endbench], axis = 1)
		Deltabench = maxDisbench - minDisbench
		FunctionalValuePart = sumDistance + Deltabench * (col-2) * L

	if gen > 5 * col:
		FunctionalValuePart = sumDistance + Delta * (col-2) * L

	FunctionalValue = sumDistance + Delta * (col-2) * L

	return subDistance, sumDistance, Delta, FunctionalValuePart, FunctionalValue


offspring = numpy.zeros(shape=(popSize, num_city))

minPathes = numpy.zeros(shape=(maxGen ,1))
minDistance = numpy.zeros(shape=(maxGen ,1))
minFvPath = numpy.zeros(shape=(maxGen, num_city))
minFv = numpy.zeros(shape=(maxGen ,1))
minDelta = numpy.zeros(shape=(maxGen, 1))

# To Obtain Each Generations Iteratively



gen = 1
pop = SampleGenerate(popSize,num_city)
subDistance, sumDistance, Delta, FunctionValuePart, FunctionValue = fitness(DisMa, pop, gen)
#print(subDistance)
print(subDistance)



























