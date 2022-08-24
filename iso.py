from distutils.log import error
from itertools import count
import pprint
from typing import Mapping


fname,fpath,output = "","",""
fContent = []
listdic = {"fileContent":[],"uLetters":[],"letters":[],"counters":[],"exactMapping":{}}


# fpath = input("target file Path\n")
fpath = "C:\\Users\\kento\\Desktop\\isolab\\"
fname = "Isomorphtest.txt"
tfile = open(fpath + fname, "r")
fContent = [line.strip() for line in tfile]
tfile.close()
# print(fContent)
listdic.update({"fileContent":fContent})


# pprint.pprint(listdic['fileContent'][0])
# pprint.pprint(listdic)

def finduLetter():
    y = 0
    counter = 0
    uLettersSize = len(listdic["uLetters"])
    
    while y < uLettersSize:   
        letterSize = len(listdic["letters"])
        localIndex = 0
        
        while localIndex < letterSize:
            #print("uLetter : " + listdic["uLetters"][y] + " letters : " + listdic["letters"][localIndex])
            if listdic["uLetters"][y] == listdic["letters"][localIndex] :
                counter += 1
            localIndex += 1
            
        y += 1
        listdic["counters"].append(counter)
        counter = 0
    
     
        
def exactMapping():
    for i in listdic["fileContent"]:#for i in filecontetn size
        index = 0 
        x=0
        wSize = len(i)
        
        while x< wSize:
            x +=1
            if i[index] not in listdic["letters"] :
                listdic["letters"].append(i[index])
                listdic["uLetters"].append(i[index])
            else :
                listdic["letters"].append(i[index])
            index += 1
            

        finduLetter()
        print(listdic["uLetters"])
        print(listdic["letters"])
        
        localMapping = ""
        localletterIndex = 0
        localuletterIndex = 0
        uLettersSize = len(listdic["uLetters"])
        letterSize = len(listdic["letters"])
        
        while localletterIndex < letterSize :
            localuletterIndex = 0
            while localuletterIndex < uLettersSize :
                if listdic["letters"][localletterIndex] == listdic["uLetters"][localuletterIndex] :
                    
                    localMapping = localMapping + str(listdic["counters"][localuletterIndex])
                localuletterIndex += 1
            localletterIndex += 1
        
        listdic["exactMapping"][i] = localMapping
        
        
        listdic["counters"].clear()      
        listdic["uLetters"].clear()
        listdic["letters"].clear()    
       
        print(" ")
    

exactMapping()
#finduLetter()
print(listdic["exactMapping"])
print("finished")