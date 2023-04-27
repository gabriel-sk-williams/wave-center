import maya.cmds as cmds
import maya.mel as mel
import random
import math
import string

#set foundational variables
pi=3.14159
cutDim=1.905 # 3/4" the thickness of a sheet of plywood
sheetWidthX=228.6 # 90"
sheetHeightY=38.1 # 15"
sheetDepthZ=cutDim # 3/4"
sheetNumber=20 # 15"
sidewall=15.24 # 6"
layers=2 #The number of unmachineed layers at the top and bottom

#create bottom two layers of plywood sheets
sCounter=0
while sCounter < layers :
    cmds.polyCube(w=sheetWidthX,h=sheetHeightY,d=sheetDepthZ,name="sheet")
    cmds.move(0,((sheetHeightY-cutDim)/2),(cutDim*sCounter)-(sheetDepthZ*2))
    sCounter=sCounter+1

#create top two layers of plywood sheets    
sCounter=sheetNumber-layers
while sCounter < sheetNumber :
    cmds.polyCube(w=sheetWidthX,h=sheetHeightY,d=sheetDepthZ,name="sheet")
    cmds.move(0,((sheetHeightY-cutDim)/2),(cutDim*sCounter)-(sheetDepthZ*2))
    sCounter=sCounter+1    

xLimit=(sheetWidthX-(sidewall*2.5))/cutDim #initial limits of interior cavity in x direction
xMax=xLimit+sidewall+sidewall 
xOriginal=xLimit #saving the original value of xLimit for future use
yLimit=sheetHeightY/cutDim  #limits of front and rear
zLimit=sheetNumber-(layers*2) #number of modified plywood sheets

counterZ=0
phaseShift=0

while counterZ < zLimit :
    
    #set a random key to use for the names of sheets
    #create a sheet and move it to the appropriate Z value    
    sheetName=''.join(random.choice(string.ascii_uppercase) for i in range(4))
    result = cmds.polyCube(w=sheetWidthX,h=sheetHeightY,d=sheetDepthZ,name=sheetName,ch=False)
    sheetName = result[0]
    cmds.move(0,((sheetHeightY-cutDim)/2),(cutDim*counterZ))
    
    #set a random key to use for names of subtractive polygons
    cubeName=''.join(random.choice(string.ascii_uppercase) for i in range(4))
    tempCube=str(cubeName)
    
    #set a random key to use for names of result of subtractive boolean function
    result=''.join(random.choice(string.ascii_uppercase) for i in range(5))
    tempResult=str(result)
    
    renderedCubeNames = list()
    phaseShift+=random.random()*.75    
    xTemp=xLimit
    
    counterY=0
    while counterY < yLimit :
        #set variables to customize the parameters of the sine wave function: period, amplitude, and phase
        period=.25
        amplitude=-4
        functionX=period*counterY  
        xLimit+=amplitude*math.sin((functionX)+phaseShift)
        diff=xMax-xLimit
        
        #create a polygon with length equal to the current x limit
        thisCubeName = cmds.polyCube(w=xOriginal*cutDim+(sidewall/3),h=cutDim,d=cutDim,name=tempCube,ch=False)
        #move the polygon to its assigned x, y, and z values
        cmds.move(diff/3-(sidewall/1.5),counterY*cutDim,(counterZ)*cutDim)
        renderedCubeNames.append(thisCubeName[0])
        counterY=counterY+1
    xLimit=xTemp  
    
    #subtract polygons at each level Z                  
    currentSheetName=sheetName
    for name in renderedCubeNames :
        returnValue = cmds.polyBoolOp(currentSheetName, name, op=2, ch=False)
        currentSheetName = returnValue[0]  
    counterZ=counterZ+1 