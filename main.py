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
popSize = 5
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
	pop[:,0] = 1
	pop[:, num-1] = num
	threshold = num/2
	for i in range(0, popSize):
		cdd = numpy.random.permutation(n) + 2
		even = cdd[numpy.array(cdd % 2 ==0,dtype='bool')]
		odd = cdd[numpy.array(cdd % 2 ==1,dtype='bool')]

		if len(even) % 2 == 1:
			extra = 1
			extraeven = next(x for x in even if x >= threshold)
		i = 1
		NodeCell = None
		# Check for initial combination
		while len(numpy.where(even >= threshold)) > 0:
			temp = next(x for x in even if x >= threshold)
			even = numpy.where(even != temp)
			print(even)
	return(extraeven)

test = SampleGenerate(5,8)
print(test)

























