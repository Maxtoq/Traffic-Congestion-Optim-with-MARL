import pandas as pd

import xml.etree.cElementTree as et
parsedXML = et.parse( "data.xml" )

dfcols = ['Id','vType','departLane' ,'arrivalLane', 'rerouteNo','timeLoss', 'stopTime', 'waitingTime', 'routeLength', 'duration']   
df = pd.DataFrame(columns=dfcols)

def getvalueofnode( node ):
	return notde.text if node is not None else None

for child in parsedXML.getroot():
	tripinfo = child.get('tripinfo')
	Id = child.attrib.get('id')
	vType = child.attrib.get('vType')
	departLane = child.attrib.get('departLane')
	arrivalLane = child.attrib.get('arrivalLane')
	rerouteNo = child.attrib.get('rerouteNo')
	timeLoss = child.attrib.get('timeLoss')
	stopTime = child.attrib.get('stopTime')
	waitingTime = child.attrib.get('waitingTime')
	routeLength = child.attrib.get('routeLength')
	duration = child.attrib.get('duration')	
	df = df.append( pd.Series( [Id,vType,departLane,arrivalLane,rerouteNo,timeLoss,stopTime,waitingTime,routeLength,
	duration],index=dfcols) ,ignore_index=True)

df.to_pickle("datastream") 
df = pd.read_pickle("datastream")
print(df)
