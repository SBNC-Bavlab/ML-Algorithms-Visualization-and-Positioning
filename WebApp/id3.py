import pickle
import copy
from queue import Queue
# import pydot
import random


class Node(object):
    def __init__(self, parentName, name, data, children, remAttr, method):
        self.parent = parentName
        self.parentPointer = None
        self.name = name
        self.data = data
        self.children = children
        self.remainingAttributes = remAttr
        self.decision = None
        self.method = method
        self.value = None


from math import log

data = pickle.load(open('car.pkl', 'rb'))
train = data['train']
test = data['test']

buyingAttr = ["vhigh", "high", "med", "low"]
maintAttr = ["vhigh", "high", "med", "low"]
doorsAttr = ["2", "3", "4", "5more"]
personsAttr = ["2", "4", "more"]
lug_bootAttr = ["small", "med", "big"]
safetyAttr = ["low", "med", "high"]
classAttr = ["unacc", "acc", "good", "vgood"]

attribNamesList = [
    "buyingAttr",
    # "maintAttr",
    # "doorsAttr",
    "personsAttr",
    "lug_bootAttr",
    "safetyAttr",
    "classAttr"
]

attribDictionary = {
    "buyingAttr": (0, buyingAttr),
    # "maintAttr": (1, maintAttr),
    # "doorsAttr": (2, doorsAttr),
    "personsAttr": (3, personsAttr),
    "lug_bootAttr": (4, lug_bootAttr),
    "safetyAttr": (5, safetyAttr),
    "classAttr": (6, classAttr)
}


# def listOfAttributes():
# 	buyingAttr = ["vhigh", "high", "med", "low"]
# 	maintAttr =  ["vhigh", "high", "med", "low"]
# 	doorsAttr = ["2", "3", "4", "5", "more"]
# 	personsAttr = ["2", "4", "more"]
# 	lug_bootAttr =  ["small", "med", "big"]
# 	safetyAttr =  ["low", "med", "high"]
# 	classAttr =  ["unacc", "acc", "good", "vgood"]

# 	attribList = [
# 		buyingAttr,
# 		maintAttr,
# 		doorsAttr,
# 		personsAttr,
# 		lug_bootAttr,
# 		safetyAttr,
# 		classAttr
# 	]

# 	return attribList

def entropy(distributionListVar, numberOfDifferentValuesVar):
    numberOfInstances = 0.0
    for dist in distributionListVar:
        numberOfInstances += dist

    if numberOfInstances == 0:
        return 0

    entropySum = 0.0
    for dist in distributionListVar:
        percentage = float(dist) / float(numberOfInstances)
        entropyHolder = 0.0
        if percentage == 0:
            entropyHolder = 0.0
        else:
            logValue = log(percentage, 4)
            entropyHolder = percentage * logValue * -1
        entropySum += entropyHolder

    return float(entropySum)


def checkAttributeValuePairMatch(attribIndexVar, attribValueVar, instanceVar):
    if instanceVar[attribIndexVar] == attribValueVar:
        return True
    return False


def getNumberOfInstancesFromLocalDistributionList(localDistributionVar):
    numberOfInstances = 0
    for value in localDistributionVar:
        if value < 0:
            absoluteVal = -value
        else:
            absoluteVal = value
        numberOfInstances += absoluteVal
    return numberOfInstances


def classifyList(attributeNameVar, instancesVar):
    attribute = attribDictionary[attributeNameVar]
    attributeIndex, attributeValues = attribute
    numberOfAttributeValues = len(attributeValues)
    localDistribution = []

    for attributeValue in attributeValues:
        counter = 0
        for instance in instancesVar:
            flag = checkAttributeValuePairMatch(attributeIndex, attributeValue, instance)
            if flag:
                counter += 1
        localDistribution.append(counter)

    return localDistribution


def getDistributionList(attributeNameVar, instancesVar):
    # build a distribution holder
    attribute = attribDictionary[attributeNameVar]
    attributeIndex, attributeValues = attribute
    numberOfAttributeValues = len(attributeValues)
    distribution = []

    # find distribution of class based of values of an attribute

    for attributeValue in attributeValues:
        localDistribution = [0, 0, 0, 0]

        for instance in instancesVar:
            flag = checkAttributeValuePairMatch(attributeIndex, attributeValue, instance)
            if flag:
                classValue = instance[-1]
                classIndex = classAttr.index(classValue)
                localDistribution[classIndex] += 1
        distribution.append(localDistribution)

    return distribution


def featureLength(attributeNameVar):
    attribute = attribDictionary[attributeNameVar]
    attributeIndex, attributeValues = attribute
    return len(attributeValues)


def information(attributeNameVar, instancesVar):
    distributionList = getDistributionList(attributeNameVar, instancesVar)
    numberOfDifferentValues = featureLength(attributeNameVar)
    # print(distributionList)
    numberOfInstances = len(instancesVar)

    informationSum = 0.0
    for localDistribution in distributionList:
        nOfInstancesInLocal = getNumberOfInstancesFromLocalDistributionList(localDistribution)
        proportionToAll = float(nOfInstancesInLocal) / numberOfInstances
        localEntropy = entropy(localDistribution, numberOfDifferentValues)

        element = proportionToAll * localEntropy
        # print(nOfInstancesInLocal, numberOfInstances, localEntropy, " = " ,element)
        informationSum += element
    return informationSum


def informationGain(attributeNameVar, instancesVar):
    distributionList = getDistributionList(attributeNameVar, instancesVar)
    numberOfDifferentValues = featureLength(attributeNameVar)
    # print (distributionList)

    # different entropy calculation
    globalDistributionList = classifyList("classAttr", instancesVar)
    entropyValue = entropy(globalDistributionList, numberOfDifferentValues)

    informationValue = information(attributeNameVar, instancesVar)
    informationGainValue = entropyValue - informationValue
    # print ("entropy:", entropyValue)
    # print ("informa:", informationValue)
    # print ("infgain:", informationGainValue)
    return informationGainValue


def logForIntrinsicInformation(proportionToAll, numberOfDifferentValues):
    if proportionToAll == 0:
        return 0
    else:
        return log(proportionToAll, numberOfDifferentValues)


def intrinsicInformation(attributeNameVar, instancesVar):
    distributionList = getDistributionList(attributeNameVar, instancesVar)
    numberOfDifferentValues = featureLength(attributeNameVar)
    # print(distributionList)
    numberOfInstances = len(instancesVar)

    intrinsicSum = 0.0
    for localDistribution in distributionList:
        nOfInstancesInLocal = getNumberOfInstancesFromLocalDistributionList(localDistribution)
        proportionToAll = float(nOfInstancesInLocal) / numberOfInstances
        logOfProportion = logForIntrinsicInformation(proportionToAll, numberOfDifferentValues)

        element = -1 * proportionToAll * logOfProportion
        intrinsicSum += element
    return intrinsicSum


def gainRatio(attributeNameVar, instancesVar):
    gainValue = informationGain(attributeNameVar, instancesVar)
    intrinsicInformationValue = intrinsicInformation(attributeNameVar, instancesVar)

    gainRatioValue = gainValue / intrinsicInformationValue
    # print("gain     :", gainValue)
    # print("intrinInf:", intrinsicInformationValue)
    # print("gainRatio:", gainRatioValue)
    return gainRatioValue


def gini(distributionListVar):
    numberOfInstances = getNumberOfInstancesFromLocalDistributionList(distributionListVar)
    if numberOfInstances == 0:
        return 0

    sumOfSquares = 0.0
    for number in distributionListVar:
        proportionToAll = float(number) / numberOfInstances
        sumOfSquares += proportionToAll ** 2
    giniValue = 1 - sumOfSquares
    return giniValue


def giniIndex(attributeNameVar, instancesVar):
    distributionList = getDistributionList(attributeNameVar, instancesVar)
    # print(distributionList)
    numberOfInstances = len(instancesVar)

    giniIndexValue = 0.0
    for localDistribution in distributionList:
        nOfInstancesInLocal = getNumberOfInstancesFromLocalDistributionList(localDistribution)
        if numberOfInstances == 0:
            proportionToAll = 0
        else:
            proportionToAll = float(nOfInstancesInLocal) / numberOfInstances
        giniValue = gini(localDistribution)

        element = proportionToAll * giniValue
        giniIndexValue += element

    return giniIndexValue


def chooseTheBest(attributeListVar, instancesVar, methodology):
    valuesList = []
    for attr in attributeListVar:
        value = 0.0
        if methodology == "gini":
            value = giniIndex(attr, instancesVar)
        elif methodology == "gainRatio":
            value = gainRatio(attr, instancesVar)
        else:
            value = informationGain(attr, instancesVar)
        valuesList.append(value)

    value = None
    if methodology == "gini":
        index = valuesList.index(min(valuesList))
        value = min(valuesList)
    else:
        index = valuesList.index(max(valuesList))
        value = max(valuesList)

    return attributeListVar[index], value


def distributeByAttribute(attributeNameVar, instancesVar):
    attribute = attribDictionary[attributeNameVar]
    attributeIndex, attributeValues = attribute
    distribution = []

    # find distribution of class based of values of an attribute
    for attributeValue in attributeValues:
        localDistribution = []

        for instance in instancesVar:
            flag = checkAttributeValuePairMatch(attributeIndex, attributeValue, instance)
            if flag:
                localDistribution.append(instance)
        distribution.append(localDistribution)

    return distribution


def childGenerator(nodeItselfVar, methodology):
    parentName = nodeItselfVar.name
    instances = nodeItselfVar.data
    remainingAttributes = nodeItselfVar.remainingAttributes
    distributedList = distributeByAttribute(parentName, instances)

    # print("~~~~~~~~~~~~~~~~~~~")
    # print(parentName)
    # print("#Insta:", len(instances) )
    # print("RemAtt:", remainingAttributes)

    parentLeafCheck = leafControl(nodeItselfVar)
    if parentLeafCheck:
        return []

    # leaf node
    if remainingAttributes == [] and instances != []:
        determineDominantOne(nodeItselfVar)
        nodeItselfVar.children = []
        return []

    # never happens, yet for safety concerns
    if instances == []:
        # print("NO instances left")
        nodeItselfVar.children = []
        return []

    # generate children
    children = []
    for dataPart in distributedList:
        childNode = Node(parentName, "", dataPart, [], [], methodology)
        childNode.parentPointer = nodeItselfVar
        isLeaf = leafControl(childNode)

        if dataPart == []:
            childNode = Node(parentName, "", dataPart, [], [], methodology)
            childNode.parentPointer = nodeItselfVar
        # print("EMPT:", childNode.parent, dataPart)

        elif isLeaf:
            childNode = Node(parentName, "", dataPart, [], [], methodology)
            childNode.parentPointer = nodeItselfVar
            determineDominantOne(childNode)
        # print("LEAF:", childNode.decision, len(childNode.data) )
        # decision = childNode.data[0][-1]

        else:
            childrenAttrName, successValue = chooseTheBest(remainingAttributes, dataPart, methodology)
            childRemainingAttrList = copy.deepcopy(remainingAttributes)
            childRemainingAttrList.remove(childrenAttrName)

            childNode = Node(parentName, childrenAttrName, dataPart, [], childRemainingAttrList, methodology)
            childNode.parentPointer = nodeItselfVar
            childNode.value = successValue
        # print("NODE:", childNode.name, len(childNode.data), childNode.remainingAttributes)

        children.append(childNode)

    # print(" ")
    # set children
    nodeItselfVar.children = children
    return children


def leafControl(nodeVar):
    distributedList = classifyList("classAttr", nodeVar.data)
    numbersGreaterThanZero = 0
    for p in distributedList:
        if p > 0:
            numbersGreaterThanZero += 1

    if numbersGreaterThanZero == 1:
        return True
    else:
        return False


def determineDominantOne(nodeVar):
    instances = nodeVar.data
    distributedListOnClassAttr = classifyList("classAttr", instances)

    maxOccurrence = max(distributedListOnClassAttr)
    maxIndexes = []
    for i in range(len(distributedListOnClassAttr)):
        if distributedListOnClassAttr[i] == maxOccurrence:
            maxIndexes.append(i)

    chosenIndex = random.choice(maxIndexes)
    dominantClassIndex = chosenIndex
    dominantClassName = classAttr[dominantClassIndex]
    nodeVar.decision = dominantClassName


def observeFromSiblings(nodeVar):
    siblings = nodeVar.parentPointer.children

    siblingsDistributions = [0, 0, 0, 0]
    for sibling in siblings:
        siblingDist = classifyList("classAttr", sibling.data)
        for i in range(len(siblingDist)):
            siblingsDistributions[i] += siblingDist[i]

    maxIndex = siblingsDistributions.index(max(siblingsDistributions))
    maxName = classAttr[maxIndex]
    nodeVar.decision = maxName


# print(nodeVar.parent, siblingsDistributions)

def treeDistribution(attributeListVar, instancesVar, methodology):
    attribListCopy = copy.deepcopy(attributeListVar)
    instancesCopy = copy.deepcopy(instancesVar)

    # this is the root node
    bestAttrName, successValue = chooseTheBest(attribListCopy, instancesCopy, methodology)
    attribListCopy.remove(bestAttrName)
    rootNode = Node("", bestAttrName, instancesCopy, [], attribListCopy, methodology)
    rootNode.parentPointer = None
    rootNode.value = successValue

    q = Queue()
    q.put(rootNode)
    while not q.empty():
        node = q.get()
        if len(node.data) == 0:
            continue
        childList = childGenerator(node, methodology)
        for child in childList:
            if leafControl(child):
                continue
            else:
                q.put(child)

    # ULFET - optimization
    reviewQ = Queue()
    reviewQ.put(rootNode)
    while not reviewQ.empty():

        node = reviewQ.get()
        for child in node.children:
            reviewQ.put(child)

        # optimize for "noInfo" nodes
        if (len(node.data) == 0):
            observeFromSiblings(node)

    return rootNode

#
# def drawFunction(rootNodeVar, fileName):
#
# 	q = Queue()
# 	v = Queue()
# 	q.put(rootNodeVar)
#
# 	text1 = \
# 		"NextAttr = " + rootNodeVar.name + r"\n" +\
# 		"#Instances = " + str(len(rootNodeVar.data)) + r"\n"
#
#
# 	nodeView = pydot.Node( text1, shape="rectangle", label=text1)
# 	v.put(nodeView)
#
# 	graph = pydot.Dot(graph_type='graph')
#
# 	level = 0
# 	while not q.empty():
# 		level += 1
# 		parentNode = q.get()
# 		parentView = v.get()
# 		children = parentNode.children
#
# 		graph.add_node(parentView)
# 		childIndex = 0
#
# 		attribute = attribDictionary[parentNode.name]
# 		attributeIndex, attributeValues = attribute
#
# 		for childNode in children:
# 			childParentAttr = attributeValues[childIndex]
# 			printParentAttr = " " + parentNode.name + "=" + childParentAttr + " "
# 			methodSuccess = " " + childNode.method + "=" + str(childNode.value) + " "
#
# 			if len(childNode.data) == 0:
# 				text1 = \
# 					"#Instances = " + str(len(childNode.data)) + r"\n" +\
# 					"Guess(assumed) = " + childNode.decision
#
# 				text2 = \
# 					"'" + printParentAttr + r"\n" + \
# 					text1 +\
# 					"Parent=" + str(level)
# 				childView = pydot.Node(text2, shape="rectangle", style="filled", fillcolor="aquamarine", label=text1)
# 			elif childNode.decision != None:
# 				text1 = \
# 					"Guess = " + childNode.decision + r"\n" + \
# 					"#Instances = " + str(len(childNode.data)) + r"\n"
# 				text2 =  \
# 					printParentAttr + r"\n" +\
# 					text1 + \
# 					"Parent=" + str(level)
# 				childView = pydot.Node(text2, style="filled", fillcolor="chartreuse", label=text1)
# 			else:
# 				text1 = \
# 					"NextAttr = " + childNode.name + r"\n" +\
# 					"#Instances = " + str(len(childNode.data)) + r"\n" +\
# 					"Value = " + str(childNode.value)
#
# 				text2 = \
# 					"'" + printParentAttr + r"\n" + \
# 					text1 + \
# 					"Parent=" + str(level)
# 				childView = pydot.Node(text2, shape="rectangle", label=text1)
#
# 			graph.add_node(childView)
# 			edgeLabel = printParentAttr
# 			edge = pydot.Edge(parentView, childView, label=edgeLabel, arrowhead="normal")
# 			graph.add_edge(edge)
# 			childIndex +=1
#
# 			if childNode.name == "":
# 				continue
# 			q.put(childNode)
# 			v.put(childView)
#
# 	graph.write_png(fileName)


def makeAGuess(rootNodeVar, testInstanceVar):
    flag = True
    node = rootNodeVar
    decision = ""
    while flag:
        if node.decision != None:
            decision = node.decision
            break
        if node.decision == None and node.name == "":
            decision = "?"
            break
        attribute = attribDictionary[node.name]
        attributeIndex, attributeValues = attribute

        featureValue = testInstanceVar[attributeIndex]
        featureIndex = attributeValues.index(featureValue)

        node = node.children[featureIndex]
    return decision


def realWorldTest(rootNodeVar, instancesVar, methodName, setName):
    valid = 0
    invalid = 0
    for ins in instancesVar:
        guess = makeAGuess(rootNodeVar, ins)
        if guess == ins[-1]:
            valid += 1
        else:
            invalid += 1
        # print (guess, ins[-1])
    print(setName, methodName, valid, invalid, (valid) / float(valid + invalid))


newAttNameList = copy.deepcopy(attribNamesList)
newAttNameList.remove("classAttr")
rootNode1 = treeDistribution(newAttNameList, train, "gini")
rootNode2 = treeDistribution(newAttNameList, train, "gainRatio")
rootNode3 = treeDistribution(newAttNameList, train, "informationGain")
'''
drawFunction(rootNode1, "gini.png")
drawFunction(rootNode2, "gainRatio.png")
drawFunction(rootNode3, "informationGain.png")
'''
'''
realWorldTest(rootNode1, train, "gini", "train")
realWorldTest(rootNode1, test, "gini", "test")
print("")

realWorldTest(rootNode2, train, "gainRatio", "train")
realWorldTest(rootNode2, test, "gainRatio", "test")
print("")

realWorldTest(rootNode3, train, "informationGain", "train")
realWorldTest(rootNode3, test, "informationGain", "test")
print("")
'''
# guess = makeAGuess(rootNode, ['low', 'med', '2', '4', 'small', 'med', 'acc'])
# print (guess)
# print(valid, invalid)

# def findTestAccuracy(testSetVar):
# iGList = []
# gRList = []
# gIList = []
# for attribName in attribNamesList:
# 	iG = informationGain(attribName, train)
# 	gR = gainRatio(attribName, train)
# 	gI = giniIndex(attribName, train)

# 	iGList.append(iG)
# 	gRList.append(gR)
# 	gIList.append(gI)

# print(attribNamesList)
# print(iGList)
# print(gRList)
# print(gIList)