import glob
import tempfile
from datetime import datetime
import warnings
import os
warnings.filterwarnings("ignore", category=FutureWarning)
import textract
from pdf2image import convert_from_path
from transformers import AutoFeatureExtractor, AutoModelForImageClassification, AutoTokenizer, AutoModelForTokenClassification, pipeline


class PreprocessFiles:
    
    def __init__(self):
        self.processor = AutoFeatureExtractor.from_pretrained("microsoft/dit-base-finetuned-rvlcdip")
        self.model = AutoModelForImageClassification.from_pretrained("microsoft/dit-base-finetuned-rvlcdip")
        self.tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
        self.model2 = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
        self.nlp = pipeline("ner", model=self.model2, tokenizer=self.tokenizer)
        
    def getEntities(self,text):
        
        try:
            out = self.nlp(text)
            return out
        except Exception as e:
            print(e)

    
    
    def getType(self, path, show=False):
        
        docType = None
        images = None

        
        if path.endswith(".docx"):
            


            pass

        elif path.endswith(".pdf"):
            images = convert_from_path(path)
            
        if images:
            
            inputs = self.processor(images=images[0], return_tensors="pt")
            outputs = self.model(**inputs)
            logits = outputs.logits

            # model predicts one of the 16 RVL-CDIP classes
            predicted_class_idx = logits.argmax(-1).item()
            docType = self.model.config.id2label[predicted_class_idx]
            
        return docType
            
            
    
        
    def getMetaData(self, path):
        
        try:
            filename, file_extension = os.path.splitext(path)
            file_extension = file_extension.replace(".","")
       
            mtime = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')
            mtime = datetime.strptime(mtime, '%Y-%m-%d %H:%M:%S').isoformat()
            dbtime = datetime.now().isoformat()
            ctime = datetime.fromtimestamp(os.path.getctime(path)).strftime('%Y-%m-%d %H:%M:%S')
            ctime = datetime.strptime(ctime, '%Y-%m-%d %H:%M:%S').isoformat()
            atime = datetime.fromtimestamp(os.path.getatime(path)).strftime('%Y-%m-%d %H:%M:%S')
            atime = datetime.strptime(atime, '%Y-%m-%d %H:%M:%S').isoformat()
            size = os.path.getsize(path)
            name = path 
            #text = self.convertPDF(path)
            d = {'name':name, 'format':file_extension,'atime':str(atime), 'mtime': str(mtime), 'ctime':str(ctime),'dbtime':str(dbtime), 'size':size/1000}
            return d
        
        except Exception as e:
            print(e)
            return e
            
    
    def convertPDF(self, path=None):
    
        try:

            with open(path, 'rb') as pdf_file:
        # Create a PDF reader object
            
                # Create an empty string variable to store the text
                text = ""

                text = textract.process(path)
                
                return text
            
        except Exception as e:
                
                return ""
        


        
    