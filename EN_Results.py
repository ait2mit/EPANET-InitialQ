#####Common errors############
# Checks no. of nodes for which results are available

# INCOMPLTE VERSION
#**********************************************************************************
#*********************Utilities****************************************************
import os
import csv
os.getcwd()

#**********************************************************************************
#***************Reading TimIndx from Matlab working directory**********************
# This is reading the value from a text file
#TimIndxTmp=open("TimIndx.txt", "r")# Time index in the report file for what we want to
#extract Data# If a single timestep data is requered that an integer can be assigned
#TimIndxRd = TimIndxTmp.readlines()
#TimIndx = TimIndxRd[0]
#TimIndx=11 # Remember index start from 0

#**********************************************************************************
#*******************Both Node and Link Common Information**************************
def NodeResults(rptFileName,ResultTimIndx,ParamIndx, RepStartTime,RepEndTime,RepInterval, N_junc, N_Res, N_Tank ):
    '''
    def NodeResults(rptFileName,ResultTimIndx,ParamIndx, RepStartTime,RepEndTime,RepInterval, N_junc, N_Res, N_Tank )
    rptFileName: EPANET report file,
    ResTimIndx: Time index for which report will be extracted
    RepStartTime: Report Start Time>>>119
    RepEndTime: Report End Time,>>120
    RepInterval: Report Enterval>>2
    N_junc: Number of Junctions>>4
    N_Res: Number of Reservoirs,>>>1
    N_Tank: Number of Tanks>>1
    "Ex_PhA3_Sc240hr.rpt"
    ResultTimIndx=0
    '''
    f= open(rptFileName, "r") 
    file_list = f.readlines()
    TimIndx=ResultTimIndx # which data I want to read. Index start from 0
    repStart=RepStartTime # Need to check in report setup
    repEnd=RepEndTime #Simulation end time, norally

    repDur=repEnd-repStart # Simulation duration
    RepInterval=RepInterval # Report time interval
    repRow=repDur/RepInterval
    spc=7 # Verified, Space between the data of each report section including all headings
    Rept=spc+repRow
    #age_inx=1 # This contral which data  Ima reading
    Qparam_indx=ParamIndx # Same as previous
    #print 'repeat',Rept
    #*************************************************************************************
    #*******************Extraction of Nodal Data******************************************
    initSkip_N=31 # Initial few lines to skip; Same for all rpt files
    LR_N=initSkip_N+TimIndx
    NoJunc=N_junc # Number of junctions # Obtain from EPANET Summary file
    NoRes=N_Res # Number of reservoirs 
    NoTank=N_Tank # Number of tanks
    TotNodes=NoJunc+NoRes+NoTank
    Age_N=[] # Initiating the list
    NodeQparam=[] # Initiating the list

    for i in range(0,TotNodes):
        
        myLine_N = file_list[LR_N:(LR_N+1)]
        #print myLine_N
        data_N = [x.replace('\n',' ') for x in myLine_N]
        #print data_N
        data_N=data_N[0].strip()
        data_N=data_N.split()
        #ag_N=float(data_N[age_inx])
        #print ag_N
        MCM_N=float(data_N[Qparam_indx])
        #Age_N.append(ag_N)
        NodeQparam.append(MCM_N) #<- Look here
        LR_N=LR_N+Rept
    return NodeQparam
        
#*****************************************************************************************
#******************************Writing Nodal data in CSV file******************************
#def NodeResults(rptFileName,ResultTimIndx,ParamIndx, RepStartTime,RepEndTime,RepInterval, N_junc, N_Res, N_Tank ):
NodeQparamN=NodeResults("Ex_PhA3_Sc240hr.rpt",0,4,119,120,2,4,1,1)
#print NodeQparamN
ndata="ndata.csv"
myfile_n = open(ndata, 'wb')
wr_n = csv.writer(myfile_n, quoting=csv.QUOTE_NONE)
wr_n.writerow(NodeQparamN) #<- Look here
myfile_n.close()   
    
#*************************************************************************************
#*******************Extraction of Link Data******************************************
def LinkResults(rptFileName,ResultTimIndx,ParamIndx, RepStartTime,RepEndTime,RepInterval, N_Links, N_Pumps, N_Valves ):
    ''' #def NodeResults(rptFileName,ResultTimIndx,ParamIndx, RepStartTime,RepEndTime,RepInterval, N_junc, N_Res, N_Tank )'''
    ff= open(rptFileName, "r")
    file_list = ff.readlines()
    TimIndx=ResultTimIndx # which data I want to read. Index start from 0
    Qparam_indx=ParamIndx # Same as previous
    repStart=RepStartTime # Need to check in report setup
    repEnd=RepEndTime #Simulation end time, norally
    RepInterval=RepInterval # Report time interval
    repDur=repEnd-repStart # Simulation duration
    repRow=repDur/RepInterval
    NoPipes=N_Links # Number of Pipes# Obtain from EPANET Summary file
    NoPumps=N_Pumps # Number of Pumps 
    NoValves=N_Valves # Number of Valves
    
    spc=7 # Verified, Space between the data of each report section including all headings
    Rept=spc+repRow
    
    # Find location of first link data
    ff= open("Ex_PhA3_Sc240hr.rpt", "r")
    for i, line in enumerate(ff, 1):
        if 'Link' in line:
            #print i
            break

    initSkip_L=i+4
    LR_L=initSkip_L+TimIndx

    TotLinks=NoPipes+NoPumps+NoValves
    #TotLinks=1
    
    LinkQparam=[] # Initiating the list
    for i in range(0,TotLinks):
        myLine_L = file_list[LR_L:(LR_L+1)]
        data_L = [x.replace('\n',' ') for x in myLine_L]
        data_L=data_L[0].strip()
        data_L=data_L.split()
        
        MCM_L=float(data_L[Qparam_indx])
        
        LinkQparam.append(MCM_L)
        LR_L=LR_L+Rept
    return LinkQparam

    
    
#def LinkResults(rptFileName,ResultTimIndx,ParamIndx, RepStartTime,RepEndTime,RepInterval, N_Links, N_Pumps, N_Valves ):  
LinkQparamL=LinkResults("Ex_PhA3_Sc240hr.rpt",0,4,119,120,2,5,0,0) 
#print LinkQparamL   
#*****************************************************************************************
#******************************Writing Nodal data in CSV file******************************   
def WriteNodeLinkResults(outFile,Node_or_Link_Results):
    try:
        ldata=outFile
        myfile_l = open(ldata, 'wb')
        wr_l = csv.writer(myfile_l, quoting=csv.QUOTE_NONE)
        wr_l.writerow(Node_or_Link_Results) #<- Look here
        myfile_l.close()
        return 0
    except:
        return 'Error: Could not Write results on file'
        
        
        
        
        
        
        
WriteNodeLinkResults('test.csv',LinkQparamL)