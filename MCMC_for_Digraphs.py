#MCMC Model
#Michael Rosenberg (mmrosenb)

#imports
import networkx as nx
import random
import copy


#helper functions

def loadIn(gmlName):
    gmlFile = open(gmlName,"rb")
    diGraph = nx.read_gml(gmlFile)
    return diGraph

def numDownArrows(seq,graph):
    downArrowCounter = 0
    for nodeInd in xrange(len(seq)):
        for nextNodeInd in xrange(nodeInd+1,len(seq)):
            (u,v) = (seq[nodeInd],seq[nextNodeInd])
            if (graph.has_edge(u,v)):
                downArrowCounter += graph.edge[u][v]["weight"]
    return downArrowCounter

#code looks very similar to previous function

def numUpArrows(seq,graph):
    upArrowCounter = 0
    #however, now we are moving backwards
    for nodeInd in xrange(len(seq)-1,-1,-1): #move down
        for prevNodeInd in xrange(nodeInd-1,-1,-1):
            (u,v) = (seq[nodeInd],seq[prevNodeInd])
            if (graph.has_edge(u,v)):
                upArrowCounter += graph.edge[u][v]["weight"]
    return upArrowCounter
        
def calculateSPi(seq,graph): #helper for calculating S(\pi)
    downArrows = numDownArrows(seq,graph)
    upArrows = numUpArrows(seq,graph)
    return (downArrows,upArrows)

def swap(a,i,j): #helper for swapping items
    (a[i],a[j]) = (a[j],a[i])

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

def producePrestigeHierarchy(seqList): #takes list of same-length sequences
    prestigeHierarchy = [0 for i in xrange(len(seqList[0]))] #length of one sequence
    for ind in xrange(len(prestigeHierarchy)):
        avgPrestige = 0
        for seq in seqList:
            avgPrestige += seq.index(ind) + 1 #add 1 to normalize starting at 1
        avgPrestige = float(avgPrestige)/len(seqList)
        prestigeHierarchy[ind] = avgPrestige
    return prestigeHierarchy

#test

graph = loadIn("History_digraph.gml")
permutationTest =  maxPermutations(graph,buff=100)
print producePrestigeHierarchy(permutationTest[0])
