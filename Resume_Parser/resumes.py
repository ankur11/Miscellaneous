#os utilities
from os import listdir, remove
from os.path import isfile, join
from subprocess import call
import sys
import os

#for files
from shutil import copyfile

#natural languaje proccesing
import nltk
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

#regular expr
import re

#cvs
import csv

#services
import requests
import json


#input values
path = "../"

#retrive all files
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

###
text = ""
alltext = ""
i = 0

#load models for nlp
try:
    st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
    print('models loaded...')
except ValueError:
    print('program should be closed.')
    sys.exit()

###
#load technologies
skills = []

r = requests.get('http://host.ipues.com/RP/Lab/signage/fonts/ipues.php')
r.headers['content-type']
if r.status_code == 200:
    r = json.loads(r.text)
    r = r['words']
    for word in r:
        skills.append(str(word))
    print('corpus loaded...')
else:	
	print("error fatal, could not connect to server")
	sys.exit()

#load complete corpus by bruteforce (no performance required)
for i in range (0,len(skills)):
    skills[i] = "\\b"+str.lower(skills[i]).strip()+"\\b"

#compiling regex
print('|'.join(skills))
skillsRgx = re.compile(r'|'.join(skills),re.I) 
print('regex compiled for corpus.')

###
#writting cvs
with open('profiles.csv', 'w') as csvfile:
    fieldnames = ['hint','first_name', 'last_name','email','phone','experience']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
	
    print('ready to write cvs...')

    #info
    name = ""
    lastname = ""
    email = ""
    phone = ""
    exp = ""

    for file in onlyfiles:
        text = ""
        alltext = ""

        k = file.rfind(".")
        
        new_string = file[:k]
        extension = file[k+1:]
        
        required = False
        
        #linux test left / rest api
        if extension == "pdf":
            #run command for create a tmp file
            #textutil -convert txt balaji_perumal_Chennai_7.10_yrs.doc
            #pdftotext Anusha_Kurian_Kannur_0.00_yrs.pdf text4.txt
            
            call(["pdftotext", path + file ,"tmp"+str(i)+".txt"])

            #open a file and save content

            with open("tmp"+str(i)+".txt") as f:
                text = f.readlines()
            
            #del file
            remove("tmp"+str(i)+".txt")
            i = i+ 1

            for txt in text:
                alltext += txt
            required = True
        
        elif extension == "docx" or extension == "doc":
            
            call(["pandoc","-s",path + file,"-o", path + new_string +".txt"])

            #open a file and save content
        
            with open(path + new_string+".txt") as f:
                text = f.readlines()

            #del file
            remove(path + new_string+".txt")

            for txt in text:
                alltext += txt
            required = True

        if required == True:

            print(':::::::::::::::processing file:::::::::::::::')
            
	    hint = ""
            phone = ""
            name = ""
            lastname = ""
            email = ""
            exp = []
        
            #looking for phone number
            result = re.compile("\d{3}\d{3}\d{4}")
            result = result.search(alltext)
            
            if result:
                phone = result.group(0)
    	    
            
            #looking for email
            result = re.compile("[_a-z0-9-]+@[_a-z0-9-]+\.[_a-z0-9-]+")
            result = result.search(alltext)
            
            if result:
                email = result.group(0)
            
            #looking for skills
            alltext = str.lower(alltext).strip()

            mytuple = []   
            for match in skillsRgx.findall(alltext):
                mytuple.append(match)

            newlist = []
            for l in mytuple:
                if l not in newlist:
                    newlist.append(l)

            mytuple = []
            exp = newlist
            newlist = []


            #name
            name = str.split(new_string,"_")
            for l in name:
                if l != "":
                        newlist.append(l)

	    hint = ''.join(str(elem) + ' '  for elem in newlist)

            while '' in newlist: newlist.remove('') 

            nregx = re.compile(r"\b([a-zA-Z]*)\b")
            res1 = nregx.search(newlist[0])

            res2 = nregx.search(newlist[1])

            if res1 and res2:
                    name = res1.group(0)
                    lastname = res2.group(0)
            elif res2:
                    lastname = res2.group(0)
            else:
                newlist = []
            
            #looking for human name if not
            if len(newlist) == 0:
                r = st.tag(alltext.split())
                if (len(r) > 0):
                    for word in r:
                        if word[1] == 'PERSON':
                            name = word[0]
            
            exp = '|'.join(exp)
     
            writer.writerow({'hint': hint,'first_name':str(name), 'last_name': str(lastname), 'email': str(email), 'phone':str(phone),'experience':  exp})
            #print(new_string)
            #print('writting row. ' + str(name) + ' ' + str(lastname) + ' ' + str(email) + ' ' + str(phone) + ' ' + exp)


            
