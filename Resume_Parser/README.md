# cvs_nlp
natural languaje processing and parsing for extracting names and experience from resumes.

# Instructions
#### 1. Make sure you have python 2.7 +
#### 2. Install the following dependencies:

  pip install -U nltk (natural languaje tool kit)

  pip install numpy

  pip install csv

  pip install requests


#### 3. Download the englis model  jar file from stanfordnlp.github.io/CoreNLP/download.html
#### 4. Download the Stanford Named Entity Recognizar 3.6.0 from nlp.stanford.edu/software/CRF-NER.shtml#Download
#### 5. set the environment variables CLASSPATH and STANFORD_MODELS as follows:


  CLASSPATH = PATH_NER_3-6-0/ner3.6.0.jar
  
  STANDFORD_MODELS = PATH_ENGLISH_MODEL.jar
  
#### 6. Install the textutil utility (e.g. for macos $brew install textutils)
#### 7. Install the pdftotext utility
#### 8. Create a directory from you have the pdfs and docs resumes and put resumes.py
#### 9. run by $ python resumes.py
#### 10. cvs file output will be created


# Notes
  



