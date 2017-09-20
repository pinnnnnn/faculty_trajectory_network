#efficient_MCMC_Model.py
#Michael Rosenberg (mmrosenb)

#imports
import networkx as nx
import random
import copy
import cPickle as cpkl


#helper functions

def loadIn(gmlName):
    gmlFile = open(gmlName,"rb")
    diGraph = nx.read_gml(gmlFile)
    return diGraph

######################## what is the seq[counter+1]??? what is the "weight" here???? When does the for loop end?
def numDownArrows(seq,graph):
    #big-Oh: n**2
    downArrowCounter = 0
    counter = 0
    for node in seq:
        for nextNode in seq[counter+1:]:
            if (graph.has_edge(node,nextNode)):
                downArrowCounter += graph.edge[node][nextNode]["weight"]
        counter += 1
    return downArrowCounter

def numUpArrows(seq,graph):
    #big-Oh: n**2
    upArrowCounter = 0
    #however, now we are moving backwards
    newSeq = copy.copy(seq)
    newSeq.reverse()
    counter = 0
    for node in newSeq: #move down
        for prevNode in newSeq[counter+1:]:
            if (graph.has_edge(node,prevNode)):
                upArrowCounter += graph.edge[node][prevNode]["weight"]
        counter += 1
    return upArrowCounter
        
def calculateSPi(seq,graph): #helper for calculating S(\pi)
    downArrows = numDownArrows(seq,graph)
    upArrows = numUpArrows(seq,graph)
    return (downArrows,upArrows)

def swap(a,i,j): #helper for swapping items
    (a[i],a[j]) = (a[j],a[i])


###################what is buff?

def maxPermutations(graph,buff): #finds permutations that maximize S(pi)
    #this function is a little long
    nodeSeq = graph.nodes() #only need number
    edgeList = graph.edges(data="True") #need weight
    random.shuffle(nodeSeq) #start off with a new nodeSeq
    maxSeqTuples = [calculateSPi(nodeSeq,graph)]
    maxSeqVal = maxSeqTuples[0][0] - maxSeqTuples[0][1] #down-up
    maxSeqList = [copy.deepcopy(nodeSeq)] #prevents aliasing
    counter = 0
    while (counter < buff):
        firstInd = random.randint(0,len(nodeSeq)-1) #or do we just care about adjacent indices?
        secondInd = random.randint(0,len(nodeSeq)-1)
        if (firstInd == secondInd): pass
        else:
            swap(nodeSeq,firstInd,secondInd)
            tempSeqTuple = calculateSPi(nodeSeq,graph)
            tempSeqVal = tempSeqTuple[0]-tempSeqTuple[1] #down-up
            if (tempSeqVal > maxSeqVal): #found new maximization!
                maxSeqTuples = [tempSeqTuple]
                maxSeqVal = tempSeqVal
                maxSeqList = [copy.deepcopy(nodeSeq)]
                counter = 0 #reset for if we get non-change
            elif (tempSeqVal == maxSeqVal): #add on
                maxSeqTuples.append(tempSeqTuple)
                maxSeqList.append(copy.deepcopy(nodeSeq))
                counter += 1
            else: #got something less than our value
                counter += 1
                swap(nodeSeq,secondInd,firstInd) #backtrack swap for MCMC
    return (maxSeqList,maxSeqTuples,maxSeqVal)

###Calculate the consensus ranking by taking the average
def producePrestigeHierarchy(seqList): #takes list of same-length sequences
###############don't understand this line specificly
    prestigeHierarchy = [0 for i in xrange(len(seqList[0]))] #length of one sequence
    for ind in xrange(len(prestigeHierarchy)):
        avgPrestige = 0
        for seq in seqList:
            avgPrestige += seq.index(ind) + 1 #add 1 to normalize starting at 1
        avgPrestige = float(avgPrestige)/len(seqList)
        prestigeHierarchy[ind] = avgPrestige
    return prestigeHierarchy


def trialRun(graph,buff):
    permutationTest =  maxPermutations(graph,buff)
    trialPrestigeHierarchy = producePrestigeHierarchy(permutationTest[0])
    return trialPrestigeHierarchy


def MCMC(gmlName,numTrials,buff):
    trialCounter = 0
    graph = loadIn(gmlName)
    prestigeDict = {}
    institutionDictionary = nx.get_node_attributes(graph,"institution")
    institutionList = []
    for nodeInd in sorted(institutionDictionary):
        institutionList.append(institutionDictionary[nodeInd]) #gives ordering
        #from least index to greatest
    for institutionName in institutionList:
        prestigeDict[institutionName] = []
    for trial in xrange(numTrials):
        print "We are on trial", trialCounter
        newPrestigeHierarchy = trialRun(graph,buff)
        for prestigeInd in xrange(len(newPrestigeHierarchy)):
            assocInstitutionName = institutionList[prestigeInd]
            prestigeDict[assocInstitutionName].append(
                        newPrestigeHierarchy[prestigeInd])
        trialCounter += 1
    prestigeFile = open("prestigeDict.pkl","wb")
    cpkl.dump(prestigeDict,prestigeFile)


MCMC("History_diGraph.gml",10000,1000)