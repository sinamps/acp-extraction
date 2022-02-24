from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging
import sys
import json
import nltk
from nltk import tag
nltk.download('punkt')

predictorCoref = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz")
with open(sys.argv[1], 'r') as f:
    contents = f.read()

result = predictorCoref.predict(
    document= contents
)
resolvedSentence = (predictorCoref.coref_resolved(contents))
a_list = nltk.tokenize.sent_tokenize(resolvedSentence)
#print(a_list)

assignment = ['contains' , 'includes' , 'include', 'contain', 'is'] 
def srl(contents):
    predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz")
    results = predictor.predict(sentence=contents)
    return results

srlList = []
for eachSentence in a_list:
        srlList.append(srl(eachSentence))
mainVerbs = []
words = []
for theElements in srlList:
        mainVerbs.append(theElements['verbs']) # This is a list where each element is for each SENTENCE.  Contains the different frames for
        words.append(theElements['words'])
elemsWithArg0 = []
elemsWithNeg = []


for i in range(len(mainVerbs)):
    for j in range(len(mainVerbs[i])):
             if("B-ARG0" in mainVerbs[i][j]['tags']):
                if("B-ARGM-NEG" in mainVerbs[i][j]['tags']):  #HAS A NEGATION IN IT 
                    elemsWithNeg.append(mainVerbs[i][j])
                elif("B-ARG0" in mainVerbs[i][j]['tags'] and "B-ARG1" in mainVerbs[i][j]['tags']):    
                    elemsWithArg0.append(mainVerbs[i][j]) 
def andSeperator(argsList):
    listtt = []
    finalList = []
    retList = argsList.split("and")
    for eachAnd in retList:
        listtt = eachAnd.split(",")
        for eachElement in listtt:
            if(eachElement != " "):
                finalList.append(eachElement)
    return finalList
    #if(argsList.find("and") != -1):
    #    retList.append(argsList[0 : argsList.find("and")])
    #    retList.append(argsList[argsList.find("and")  + 3 : ])
    #else:
    #    retList.append(argsList)
    #return retList
correctAssociations = []
correctAssignments = [] 
arg1List = []
## CREATING THE ASSOCICATION AND ASSIGNMENT RELATION 
for elements in elemsWithArg0: 
    description = elements['description'] ## description': '[ARG0: HCP] [V: adds] [ARG1: an office visit] .'
    indexargs0 = description.index('ARG0')
    indexargs1 = description.index('ARG1')
    args0 =  description[indexargs0 + 6: description.find("]", indexargs0 )] #HCP
    args1 =  description[indexargs1 + 6: description.find("]" , indexargs1 )] # an office visit
    arg0List = andSeperator(args0)  ## Multiple argument0s that all have Argument1 
    arg1List = andSeperator(args1)  #If there are multiple argument1s, all of them have arg0(s).
   
    for elements0 in arg0List:   ## for each ARG0
        for elements1 in arg1List: ##assign each arg1 to an Arg0
            if(elements['verb'] in assignment): ##check if it is assignment
                    correctAssignments.append('(' + elements0 +',' + elements1 + ')')   ##assignment relation
                    continue
            correctAssociations.append(elements0+ '--' + elements['verb'] + '--' + elements1)
            print(correctAssociations[-1] + "\n")
            

    
#print('Association relations - \n')
#for stuff in correctAssociations:
#    print(stuff)



##CREATING PROHIBITION FUNCTIONS 
prohibitions = []
for elements in elemsWithNeg:
    description = elements['description']
    indexargs0 = description.index('ARG0')
    indexargs1 = description.index('ARG1')
    args0 =  description[indexargs0 + 6: description.find("]", indexargs0 )]
    args1 =  description[indexargs1 + 6: description.find("]" , indexargs1 )]
    arg0List = andSeperator(args0)
    arg1List = andSeperator(args1)
   
    for elements0 in arg0List:
        for elements1 in arg1List:
            prohibitions.append('ua_deny(' + elements0 + ',' + elements['verb'] + ',' + elements1 + ')' )
print("Prohibition relations - \n" )
for stuff in prohibitions:
    print(stuff)


print("Assignment relations - \n" )
for stuff in correctAssignments:
    print(stuff)
  
with open('theRelations.txt', 'w') as file:
    for item in correctAssociations:
        file.write("%s\n" % item)


with open('demo.txt', 'w') as f:
    for item in mainVerbs:
        f.write("%s\n" % item)
f.close()
file.close()
