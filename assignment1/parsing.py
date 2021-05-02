import re
import os
import zipfile

class file_with_pos(object):
    def __init__(self, fp):
        self.fp = fp
        self.pos = 0
    def read(self, *args):
        data = self.fp.read(*args)
        self.pos += len(data)
        return data
    def tell(self):
        return self.pos

       
#helper function to retreive unique docs with term  
def numOfDocs(searchTerm):
    selected_elements = []
    for index in termInfo[searchTerm]:
        if index[0] in selected_elements:
            pass
        else:
            selected_elements.append(index[0])
    #print(selected_elements)
    return len(selected_elements)

#get positions of a term within a doc
def getPositions(termVal,docVal):
    positionList = []
    for index in termInfo[termVal]:
        if index[0] == docIndex[docVal][0]:
            positionList.append(index[1])
    return positionList

#get frequency of termVal within docVal
def getFrequency(termVal,docVal):
    counter = 0
    for index in termInfo[termVal]:
        if index[0] == docIndex[docVal][0]:
            counter = counter + 1
    return counter

#get term data
def getTerm(termVal):
    print("Listing for term: " + termVal)
    if termVal in termIndex:
        print("TERMID: " + str(termIndex[termVal][1]))
        print("Number of documents containing term: " + str(numOfDocs(termVal)))
        print("Term frequency in entire corpus: " + str(termIndex[termVal][0]))
    else:
        print("TERM IS NOT IN ANY DOCS")
#print(termInfo)

#get doc data
def getDoc(docVal):
    print("Listing for document: " + docVal)
    if docVal in docIndex:
        print("DOCID: " + str(docIndex[docVal][0]))
        print("Distinct terms: " + str(docIndex[docVal][2]))
        print("Total terms: " + str(docIndex[docVal][1]))

#get inverted list data
def getInverted(docVal, termVal):
    print("Inverted list for term: " + termVal)
    print("In document: " + docVal)
    if docVal in docIndex:
        if termVal in termIndex:
            print("TERMID: " + str(termIndex[termVal][1]))
            print("DOCID: " + str(docIndex[docVal][0]))
            print("Term frequency in document: " + str(getFrequency(termVal,docVal))) 
            posList = getPositions(termVal,docVal)
            if posList:
                print("Positions: " + str(posList)[1:-1]) 
            else:
                print("Positions: Does not exist")

# Regular expressions to extract data from the corpus
doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)


with zipfile.ZipFile("ap89_collection_small.zip", 'r') as zip_ref:
    zip_ref.extractall()
   
# Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
for dir_path, dir_names, file_names in os.walk("singlefiletest"):
    allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]
    
counter = 1
termCounter = 1;    
docIndex = {}
termIndex = {}
termInfo = {}
for file in allfiles:
    with open(file, 'r', encoding='ISO-8859-1') as f:
        filedata = f.read()
        result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch documents
        for document in result[0:]:
            # Retrieve contents of DOCNO tag
            docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
            # Retrieve contents of TEXT tag
            text = "".join(re.findall(text_regex, document))\
                      .replace("<TEXT>", "").replace("</TEXT>", "")\
                      .replace("\n", " ")
            
            # step 1 - lower-case words, remove punctuation, remove stop-words, etc.
            docno = docno.lower()
            text = text.lower()
            #print doc and create unique tag
            #print(str(counter) + ", " + docno)
            

            characters_to_remove = "!@#$%^&*()-_=+:;\"'<>?,./~`"
            for character in characters_to_remove:
                text = text.replace(character,"")
            text = text.split()
            f = open("stopwords.txt",'r')
            f = f.read().split()
            #print(f)
            #step 2 - create tokens 
            text = [w for w in text if not w in f]
            #push doc ID and amount of terms per doc
            docIndex[docno] = []
            docIndex[docno].append(counter)
            docIndex[docno].append(len(text))
            selected_elements = []
            for index in text:
                if index in selected_elements:
                    pass
                else:
                    selected_elements.append(index)
            docIndex[docno].append(len(selected_elements))
           
            #print(text)
            # step 3 - build index
            posCnt = 1
            #docHasTerm = false
            for item in text:
                if item in text:
                    if item not in termInfo:
                        #push item into termInfo and termIndex
                        termInfo[item] = []
                        termIndex[item] = []
                        #create termindex (total count, termID)
                        termIndex[item].append(0)
                        termIndex[item].append(termCounter)
                        termCounter = termCounter + 1
                    if item in termInfo:
                        #if item is accounted for, push the read pos and increase count
                        termList = [counter,posCnt]
                        termInfo[item].append((termList))
                        termIndex[item][0] = termIndex[item][0] + 1

                posCnt = posCnt + 1
            counter = counter + 1

#write to docids
with open('docids.txt','w') as docText:
    for doc in docIndex:
        docText.write("%s\t%s\n" % (docIndex[doc][0],doc))
docText.close()

#write to term_index
with open('term_index.txt','w') as termIndexText:
    for term in termInfo:
        termIndexText.write("%s" % termIndex[term][1])
        for index in termInfo[term]:
            termIndexText.write("\t%s:%s" % (index[0],index[1]))
        termIndexText.write("\n")
termIndexText.close()

#write to termids
with open('termids.txt','w') as termText:
    for term in termIndex:
        termText.write("%s\t%s\n" % (termIndex[term][1],term))
docText.close()

#write to 
with open('term_info.txt','w') as termInfoText:
    with open('term_index.txt','r') as termIndexText:
        for term in termIndex:
            termID = termIndex[term][1]
            offset = termIndexText.tell()
            termIndexText.readline()
            totalAmt = termIndex[term][0]
            totalDocs = numOfDocs(term)
            termInfoText.write("%s\t%s\t%s\t%s\n" % ((str(termID)),str(offset),str(totalAmt),str(totalDocs)) )
    termIndexText.close()
termInfoText.close()

