import csv

''' 
This module defined a function to extract all the nodes and links names from the .inp file
'''

def get_line_number(inpfile, phrase):
    with open(inpfile) as f:
        for i, line in enumerate(f, 1):
            if phrase in line:
                return i


#*************************************************************************************
#*******************Extraction of Nodes/Pipes as per Index******************************************

def NodeLinkAsPerIndex(inpfile, phrase,NodesPipesNo):
    f= open(inpfile, "r") 
    file_list = f.readlines()
    lineNo4Jun=get_line_number(inpfile,phrase)
    #return lineNo4Jun

    LR_N=lineNo4Jun+1
    NoJunc=NodesPipesNo # Number of junctions # Obtain from EPANET Summary file
    allNodes=[] # Initiating the list

    for i in range(0,NoJunc):
        myLine_N = file_list[LR_N:(LR_N+1)]
        data_N = [x.replace('\n',' ') for x in myLine_N]
        #print data_N
        data_N=data_N[0].strip()
        data_N=data_N.split()

        allNodes.append(data_N[0]) #<- Look here
        LR_N=LR_N+1
       
    return allNodes    




