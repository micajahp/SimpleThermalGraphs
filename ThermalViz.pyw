### Select File to Load 

#Load File

### Select More Files or Continue?
# Load File
# Create Data Set Difference
# Create Data Set Average
import sys

import datetime
import os
import easygui
import time
import numpy as np


import plotly.graph_objects as go
from plotly.subplots import make_subplots
from colorama import Fore,init                   ## For fancy prints to console
init(autoreset="True")

#datetime.strptime()
nowish = time.time()
Files_Loaded = 0


fig1 = go.Figure()
fig1 = make_subplots(specs=[[{"secondary_y": True}]])
fig1.update_layout(newshape_layer="below",template = "plotly_dark")



def ListFiles(FilePath = "./"):
    
    FileList = []
    #print(f"{Fore.GREEN}{FilePath[-1]}")
    if FilePath[-1] != '/' and FilePath[-1] != '\\': 
        #print(f'Generating File Path from {FilePath}\n')
        
        #print(f"{FilePath}")
        q = 0
        p = 0
        for i in enumerate(FilePath):
            if "\\" in i:
                p = q
                print(f"{i}\n")
                print(f"{p}\n")
            q +=1 
        print(FilePath[0:p+1])
        FilePath = FilePath[0:p+1]
        
        #print(f'Finished {FilePath}\n')
        
        
    ListOfFiles = os.listdir(FilePath)
    for items in ListOfFiles:
        if '.csv' in items:
            #print(f"{FilePath + items}")
            FileList.append(FilePath + items)
            #print(f"{Fore.CYAN}{FileList}")
    return FileList
    
    
    
def LoadData(FileName):
    
    
    Xaxis = []
    with open(FileName,"r") as r:
        Legend = r.readline()
        Legend = Legend.replace("\n","")
        
        Legend = Legend.split(",")
    Axis_List = {}
    print(Legend)
    
    Axis_List = {f"TimeStamp" : 0}
    #####################################################################################
    # All Options for Chamber Log output Listed
    
    for i in Legend: 
        if Legend.index(i) != 0:
                
            if i == '':
                break   
            Axis_List[f"{i}"] = Legend.index(i)
            
            print (f"{i} : {Legend.index(i)}")
    Yaxis = dict()
    for i in Axis_List:
        print(f"{Fore.GREEN}{i}{Fore.WHITE} in column {Fore.YELLOW}{Axis_List[i]}")
        Yaxis[i] = []
        
        
    with open(FileName,"r") as r:
        datadata = r.readline()
        while(datadata):
            datadata = r.readline()
            if(datadata == ''):
                break
            datadata = datadata.replace("\n","")
            datadata = datadata.split(",")
            
            #print(Axis_List)
            for i in Axis_List:
            
                if('TimeStamp' not in i):
                    Yaxis[i] += [  float(  datadata[  Axis_List[ i ]  ]  )  ]
                    
                if('TimeStamp' in i):
                    
                    try:
                        xtemp = datetime.datetime.fromtimestamp(int(datadata[Axis_List[f"TimeStamp"]]))
                        Xaxis.append(xtemp.strftime('%Y-%m-%d %H:%M:%S'))
                    except:
                        Xaxis.append(datadata[Axis_List[f"TimeStamp"]])
    return [Axis_List,FileName[-8:-4],Xaxis,Yaxis]
    
def Difference(Xaxis1,Xaxis2,Yaxis1,Yaxis2,C1,C2,Axis_Dict):

    Diff = []
    a = len(Xaxis1)
    b = len(Xaxis2)
    if a>b:
        a=b
    for ii in range(a):
        print(f'{Fore.CYAN}C1 = {Yaxis1[f"{C1}"][ii]}  {Fore.RED}C2 = {Yaxis2[f"{C2}"][ii]}  {Fore.GREEN}D = {Yaxis1[f"{C1}"][ii]-Yaxis2[f"{C2}"][ii]}')
        Diff.append(float(Yaxis1[f"{C1}"][ii])-float(Yaxis2[f"{C2}"][ii]))
    print(Diff[-1])
    return Diff
    
    
    
    
def Averages(Xaxis,Yaxis,AVGLIST,Axis_Dict):
    print(type(Axis_Dict))
    Summation = []
    print(AVGLIST)
    if(len(AVGLIST) <= 1):
        return [0]
    else:
        a =  np.inf
        for i in Xaxis:
            if a>len(i):
                a = Xaxis.index(i)
        print
        for i in range(len(Xaxis[a])-1):
            temp = 0
            
            for item in AVGLIST:
                
                temp += Yaxis [item[1]] [item[0]] [i]
            
            Summation.append(temp/len(AVGLIST))
            Average = np.array(Summation)
            Avg2 = Average.tolist() 
            
        Axis_Dict[-1][f"Avg{AVGLIST}"] = len(Axis_Dict[0])
        Yaxis.append(dict())
        for item in Yaxis:
            print(f"{Fore.RED}{item}")
            print(f"{Fore.GREEN}{item}")
        Yaxis[-1]["Avg"] = []
        Yaxis[-1]["Avg"] += Avg2
        print(f"{Fore.GREEN}{Axis_Dict}")
    return [ Xaxis, Yaxis, Axis_Dict]

    
def GraphIt(Xaxis,Yaxis,Columns):

    
    print(Columns)
    
    print(len(Yaxis))
    print(len(Xaxis))
    try:
        print("")
        #print(f"{Fore.MAGENTA}{Yaxis}")
    except:
        pass
    for i in Columns:
        
        #if type(Columns) == "<class 'dict'>":
        try:
            iindex = Columns[i]
        except:
            print(type(Columns))
            iindex = Columns.index(i)
            print(len(Yaxis[iindex]))
        if("TimeStamp" not in i):
            if("Different" in i):
                fig1.add_trace(go.Scatter(x = Xaxis, y=Yaxis[iindex],name=f"Difference",mode='markers', marker={'size':2}),secondary_y=True)
            else:
                if ("Different" in Columns):
                    try:
                        # print(iindex)
                        fig1.add_trace(go.Scatter(x = Xaxis, y=Yaxis[iindex],name=f"{i}",mode='markers', marker={'size':2}),secondary_y=False)
                    except:
                        iindex = Columns.index(i)
                        # print(f"{iindex}2")
                        
                        fig1.add_trace(go.Scatter(x = Xaxis, y=Yaxis[iindex],name=f"{i}",mode='markers', marker={'size':2}),secondary_y=False)
                else:
                    # print("No index")
                    if "Press" in i:
                        fig1.add_trace(go.Scatter(x = Xaxis, y=Yaxis[i],name=f"{i}",mode='markers', marker={'size':2}),secondary_y=True)
                    else:
                        if "Lines" in i: 
                            fig1.add_trace(go.Scatter(x = Xaxis, y=Yaxis[i],name=f"{i}",mode='lines', marker={'size':2}),secondary_y=False)
                        else:
                            fig1.add_trace(go.Scatter(x = Xaxis, y=Yaxis[i],name=f"{i}",mode='markers', marker={'size':2}),secondary_y=False)
                            
    fig1['layout']['yaxis'].update(autorange = True)    
    fig1.write_html(f"{int(nowish)%10000}fig.html")
    fig1.show()
    

    
if __name__ == "__main__":
    Files_List = ListFiles()
    Columns=[]
    prependStr=[]
    Xaxis=[]
    Yaxis=[]
    while(True):
        if Files_Loaded == 0:
            Choice = easygui.buttonbox("Select to Contine","TermalVizualizer",["Load File","Cancel"])
        else:
            Choice = easygui.buttonbox("Select to Contine","TermalVizualizer",["Load File","Create Data Set\nDifference","Create Data Set\nAverage","Graph","Exit"])
        
        
        
        
        match Choice:
            case "Create Data Set\nAverage":
                AVGLIST = []
                C1 = 'Pick'
                while (C1 != None):
                    if (len(Columns) > 1):
                    
                        i = easygui.choicebox("Select File", "From Which File", range(len(Columns)))
                        print(i)
                        
                        try:
                            i = int(i)
                            C1   = easygui.choicebox("Channel To Average", "Select A Channel", Columns[i])
                            print(f"{Fore.YELLOW}{C1}")
                                
                                
                            if C1 in Columns[i]:
                                AVGLIST.append([C1,i])
                        except:
                            if(i == None):
                                C1 = None
                                print("Exiting Choice")
                        print(C1,i)
                        
                        
                        
                    else:
                        i = 0
                        C1 =   easygui.choicebox("Channel To Average", "Select A Channel", Columns[i])
                        print(f"{Fore.YELLOW}{C1}")
                        try:
                            i = int(i)
                        except:
                            print("Exiting Choice")
                        if C1 in Columns[i]:
                            AVGLIST.append([C1,i])
                print(f"{Fore.MAGENTA}{C1}:Needs Added to List")      
                if(C1 == None ):            
                    #print(f"[{len(Xaxis)},{len(Yaxis)},{AVGLIST},{Columns}")
                    AVG = Averages(Xaxis,Yaxis,AVGLIST,Columns)
                    #print(f"{Fore.MAGENTA}{AVG}")
                    Xaxis = AVG[0]
                    Yaxis = AVG[1]
                    Columns = AVG[2]
                    Files_Loaded+=1
                
                
                
                
                
            case 'Load File':
               
                Big_List= LoadData(easygui.buttonbox("Select to Contine","TermalVizualizer",Files_List))
                Columns.append(Big_List[0])
                prependStr.append( Big_List[1])
                Xaxis.append(Big_List[2])
                Yaxis.append(Big_List[3])
            
                # Load The Data From The File
                
                Files_Loaded += 1
            case "Graph":
                print(f"{Fore.GREEN}{Columns}")
                for i in range(len(Columns)):
                    print(f"{Fore.RED}i : {len(Columns)}")
                    GraphIt(Xaxis[i],Yaxis[i],Columns[i])
                    
                    
            case "Create Data Set\nDifference":
                print(Columns)
                if (len(Columns) > 1):
                    i = easygui.choicebox("Select File", "From Which File", range(len(Columns)))
                    i = int(i)
                    C1   = easygui.choicebox("Select Base Channel", "This One Minus The Next One", Columns[i])
                    ii = easygui.choicebox("Select File", "From Which File", range(len(Columns)))
                    ii = int(ii)
                    C2   = easygui.choicebox("Select Second Channel", "The First One Minus This One", Columns[ii])
                else:
                    i = 0
                    C1 =   easygui.choicebox("Select Base Channel", "This One Minus The Next One", Columns[i])
                    ii = 0
                    C2 =   easygui.choicebox("Select Second Channel", "The First One Minus This One", Columns[ii])
                Different = Difference(Xaxis[i],Xaxis[ii],Yaxis[i],Yaxis[ii],C1,C2,Columns)
                Columns.append([C1,C2,"Different"])
                if (len(Xaxis[i]) > len(Xaxis[ii])):
                    Xaxis.append(Xaxis[i])
                    Xaxis.append(Xaxis[ii])
                    Xaxis.append(Xaxis[ii])
                else:
                    Xaxis.append(Xaxis[i])
                    Xaxis.append(Xaxis[ii])
                    Xaxis.append(Xaxis[i])
                Yaxis.append([Yaxis[i][f"{C1}"],Yaxis[ii][f"{C2}"],Different])
                

                    
                    
                
                
            case _:
                quit()
                exit()
                sys.exit()
                sys.quit()
    