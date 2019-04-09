import pandas as pd
import xml.etree.cElementTree as et


class Data_parsed_file:

	
	def __init__ (self,name,id_list):
		self.name = name
		self.id_list = id_list
		parsedXML = et.parse(name)
		dfcols = ['Id','vType','departLane' ,'arrivalLane','timeLoss', 'waitingTime', 			'routeLength', 'duration']   
		df = pd.DataFrame(columns=dfcols)
		for child in parsedXML.getroot():
			tripinfo = child.get('tripinfo')
			Id = int(child.attrib.get('id'))
			vType = child.attrib.get('vType')
			departLane = child.attrib.get('departLane')
			arrivalLane = child.attrib.get('arrivalLane')
			timeLoss = child.attrib.get('timeLoss')
			waitingTime = child.attrib.get('waitingTime')
			routeLength = child.attrib.get('routeLength')
			duration = child.attrib.get('duration')	
			if Id in id_list:				
				df=df.append( pd.Series( [Id,vType,departLane,arrivalLane,
					timeLoss,waitingTime,routeLength,
					duration],index=dfcols) ,ignore_index=True)
		print(df)



				


	
	def getvalueofnode( node ):
		return notde.text if node is not None else None

a = Data_parsed_file("data.xml", [1, 3])

