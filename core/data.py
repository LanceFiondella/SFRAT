
def convertFileData(inputData):
	'''
	takes in raw pandas dict, converts to T/IF/FT/FI dict
	'''
	outData = {}
	for sheet in inputData:

		newFrame = {}
		keys = inputData[sheet].keys()

		if 'T' in keys:
			newFrame['FN'] = inputData[sheet]['T'].copy()
		elif 'FN' in keys:
			newFrame['FN'] = inputData[sheet]['FN'].copy()

		if 'IF' in keys:
			newFrame['IF'] = inputData[sheet]['IF'].copy()
		elif 'FC' in keys:
			newFrame['IF'] = inputData[sheet]['FC'].copy()

		if 'FT' in keys:
			newFrame['FT'] = inputData[sheet]['FT'].copy()
		elif 'CFC' in keys:
			newFrame['FT'] = inputData[sheet]['CFC'].copy()

		if 'IF' in newFrame.keys() and not 'FT' in newFrame.keys():
			# sheet has IF, convert for FT/CFC
			newFrame['FT'] = [newFrame['IF'][0]]
			for idx in range(1,len(newFrame['IF'])):
				newFrame['FT'].append(newFrame['FT'][idx - 1] + newFrame['IF'][idx])
			print(f'{sheet} missing FT, calc from IF')
		elif 'FT' in newFrame.keys() and not 'IF' in newFrame.keys():
			newFrame['IF'] = [newFrame['FT'][0]]
			for idx in range(1,len(newFrame['FT'])):
				newFrame['IF'].append(newFrame['FT'][idx] - newFrame['FT'][idx - 1])
			print(f'{sheet} missing IF, calc from FT')

		newFrame['FI'] = []
		for fi in newFrame['IF']:
			if fi == 0:
				newFrame['FI'].append(-1)
				continue
			newFrame['FI'].append(1/fi)
		mx = max(newFrame['FI'])
		for i, fi in enumerate(newFrame['FI']):
			if fi == -1:
				newFrame['FI'][i] = float('inf')
				#newFrame['FI'][i] = 2*mx # todo make this better

		outData[sheet] = newFrame

	return outData
	