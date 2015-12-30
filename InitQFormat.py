'''
Goal: Reduce Simulation Time fro extra large water network 
Objectives: To configure EPANET-MSX file based on intermediate results so that simulation can be run for a stable network based on 
calculated initial concentration
Dependency: This module depends on other two modules (i)extractNodeLinkList, (ii) EN_Results. This two modules must be stored in
the environment

UDF: User defined parameter: This parameters must be updated for each individual networks and simulation
'''

import csv
import pandas as pd
import numpy as np
import extractNodeLinkList as ENL # Module developed to extract List of Links and Nodes based  as per index
import EN_Results as ER # Module developed to get particular species results

##### All the files#############################
inpfile="exampletank.inp"       # EPANET *.inp file                                                                         #UDP:1 
msxfile="Ex_PhA3_Sc.msx"        # EPANET *.msx file                                                                         #UDP:2
rptfile="Ex_PhA3_Sc120hr.rpt"   # EPANET *.rpt file                                                                         #UDP:3
N_junc=4                        # Number of Junctions Read from EPANET summary                                              #UDP:4
N_Res=1                         # Number of Reservoir from EPANET summary                                                   #UDP:5
N_Tank=1                        # Number of Tanks from EPANET summary                                                       #UDP:6
N_Pipes=5                       # Number of Pipes,if any WALL species exist, Not revelevant in this study                   #UDP:7*
N_Pumps=0                       # Number of pumps, if any WALL species exist, Not revelevant in this study                  #UDP:8*
N_Valves=0                      # Number of Valves, if any WALL species exist, Not revelevant in this study                 #UDP:9*
#def LinkResults(rptFileName,ResultTimIndx,ParamIndx, RepStartTime,RepEndTime,RepInterval, N_Pipes, N_Pumps, N_Valves ): 
ResultTimIndx=0                 # Index of Results to be reported in *rpt file                                              #UDP:10
RepStartTime=119                # Report start time                                                                         #UDP:11
RepEndTime=120                  # Simulation Duration                                                                       #UDP:12
RepInterval=2                   # Report time interval                                                                      #UDP:13
#def NodeResults(rptFileName,ResultTimIndx,ParamIndx, RepStartTime,RepEndTime,RepInterval, N_junc, N_Res, N_Tank )


###################################################

NodesOrPipes="Junctions"
NodesNo=N_junc # Number of junctions # Obtain from EPANET Summary file                   
allNodesInx =ENL.NodeLinkAsPerIndex(inpfile,NodesOrPipes.upper(),NodesNo)

NodesOrPipes="TANK"
TanksNo=N_Tank                                                                           
if TanksNo!=0:
    allTanksInx =ENL.NodeLinkAsPerIndex(inpfile,NodesOrPipes.upper(), TanksNo)
else:
    allTanksInx=0
    
NodesOrPipes="Reservoir"                                                            
ResNo=N_Res
allResInx =ENL.NodeLinkAsPerIndex(inpfile,NodesOrPipes.upper(), ResNo)
if TanksNo!=0:
    allJuncInx=allNodesInx+allResInx+allTanksInx
else:
    allJuncInx=allNodesInx+allResInx

allNodeListDF=pd.DataFrame(allJuncInx)

##############SPECIES LIST##########################
#msxfile="Ex_PhA3_Sc.msx"
f= open(msxfile, "r") 
file_listMSX = f.readlines()
#f.close()
speciesList=[]
for line in file_listMSX:
    words=line.strip().split()
    if "BULK" in words:
        spcs=words[1]
        speciesList.append(spcs)

#print speciesList
##########################################

### Extracting Nodal Results####################

#rptfile="Ex_PhA3_Sc120hr.rpt"
#NodeResSP4=ER.NodeResults(rptfile,0,4,119,120,2,4,1,1)

nodeText = pd.DataFrame(["NODE"] *len(allNodeListDF))
speciesTextNode=pd.DataFrame([speciesList[0]] *len(allNodeListDF))
#print speciesTextNode
##################################################################
####Making Dataframe in format to set Initial Quality
listSpcsDF=[]
for i in range(0,len(speciesList)):
    speciesTextNode=pd.DataFrame([speciesList[i]] *len(allNodeListDF))    
    NodeResSP=ER.NodeResults(rptfile,ResultTimIndx,i+1,RepStartTime,RepEndTime,RepInterval,N_junc,N_Res,N_Tank)
    NodeResSP4DF=pd.DataFrame(NodeResSP)
    ptr= pd.concat([nodeText, allNodeListDF, speciesTextNode,NodeResSP4DF], axis=1)
    listSpcsDF.append(ptr)
InitQDF=pd.concat(listSpcsDF)

######################Convert DataFrame to String without Index and Header
InitQStr= InitQDF.to_string(index=False, header=False)
#print InitQStr

#################Find Location of [QUALITY] string#################
f.seek(0) # Take the cursor at the begining
for qLoc, line in enumerate(f, 1):
    if 'QUALITY' in line:
        #print qLoc
        break

#print 'Location:',qLoc

f.close()





file_listMSX.insert(qLoc, InitQStr)

f = open("nw.msx", "w") # New MSX file with all the initial Quality setup
file_listMSX = "".join(file_listMSX)
f.write(file_listMSX)
f.close()



'''
pt="toPaste.csv" # Pipe species in fact not necesssary. Only required when there is a wall species Ref: epanetmsx manual page 
ptr.to_csv(pt, sep='\t', encoding='utf-8', index = False, header=False)
'''