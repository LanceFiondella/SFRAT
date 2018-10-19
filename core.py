
import pandas as pd
import logging as log


def DataFormat(dataclass):	#supply pd data object, formats/completes dataset

	if not 'FT' in dataclass:
		dataclass['FT'] = dataclass['IF']
		for i in range(1,len(dataclass)):
			dataclass['FT'][i] += dataclass['FT'][i-1]

	elif not 'IF' in dataclass:
		dataclass['IF'] = dataclass['FT']
		for i in range(len(dataclass)-1,0,-1):
			dataclass['IF'][i] -= dataclass['IF'][i-1]

	else:
		log.info('Input data does not contain IF or FT')

	return dataclass #either just run method or set var to method result


def LaplaceTest(dataclass):	#returns series object of size dataclass.size with laplace values
	laplace = pd.Series(0) #0 gives workable series

	for i in range(2,len(dataclass)):
		cur_sum = sum(dataclass['FT'][1:i])
		laplace[i] = (((1/(i-1))*cur_sum) -(dataclass['FT'][i]/2))/(dataclass['FT'][i]*(1/(12*(i-1))**(0.5)))

	return laplace

def AverageTest(dataclass):
	avg = pd.Series(0)

	for i in range(len(dataclass)):
		avg[i] = sum(dataclass['FT'][0:i+1])/(i+1)

	return avg

ex = pd.read_excel('model_data.xlsx')
ex['new'] = AverageTest(ex)
print(ex)