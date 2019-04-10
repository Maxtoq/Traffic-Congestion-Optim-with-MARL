import pandas as pd
import xml.etree.cElementTree as et

class DataParser:

	def __init__ (self, name, id_list=None):
		self.name = name
		self.id_list = id_list

		parsedXML = et.parse(name)

		dfcols = ['Id','departLane' ,'arrivalLane','timeLoss', 
				  'waitingTime', 'routeLength', 'duration']   
		df = pd.DataFrame(columns=dfcols)
		
		for child in parsedXML.getroot():
			Id = child.attrib.get('id')
			departLane = child.attrib.get('departLane')
			arrivalLane = child.attrib.get('arrivalLane')
			timeLoss = child.attrib.get('timeLoss')
			waitingTime = float(child.attrib.get('waitingTime'))
			routeLength = child.attrib.get('routeLength')
			duration = float(child.attrib.get('duration'))

			if self.id_list is not None:
				if int(Id) in self.id_list:				
					df = df.append(pd.Series([Id, departLane, arrivalLane,
									timeLoss, waitingTime, routeLength,
									duration], index=dfcols), ignore_index=True)
			else:
				df = df.append(pd.Series([Id, departLane, arrivalLane,
                                    timeLoss, waitingTime, routeLength,
                                    duration], index=dfcols), ignore_index=True)

		print(df)
		print('Mean waiting time = ' + str(df['waitingTime'].mean()))
		print('Mean travel time = ' + str(df['duration'].mean()))

	def getvalueofnode(self, node):
		return node.text if node is not None else None


