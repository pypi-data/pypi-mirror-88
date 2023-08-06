from glob import glob
import os
from PIL import Image

import torch
import torchvision
from torchvision import models, transforms

from PyPDF2 import PdfFileMerger
import shutil 




class bieza:


    #converter = ConverterAndSpilt()
    document_class = {0: 'certificate', 1: 'other', 2: 'resume', 3: 'transcript'}
    model = torch.load(r"PredictionModel.pt") #โมเดลจากการทำ image classification
    predicteddir = r"multipagedocclassify\DocDirectory\predictedfile" #โฟลเดอร์ที่จัดเก็บไฟล์ต้นฉบับ
    outputdir = r"multipagedocclassify\DocDirectory\TMPfile\docclass" #ที่เก็บไฟล์ชั่วคราวที่ทำนายผลแล้วเป็น PDF
    
    doc_extension = [".doc", "docx"]
    image_extension = [".gif", ".jfif", ".jpeg", ".jpg", ".BMP", ".png"]



    def predictIMG(self, inputpath): #ทำนายผลจากโมเดลที่ได้มาจาก image classification

        image_transforms = { 
            'test': transforms.Compose([
                transforms.Resize(size=(256,256)),
                transforms.CenterCrop(size=224),
                transforms.Grayscale(3),
                transforms.ToTensor(),
            ])}
            
            
        transform = image_transforms['test']
        
        image = Image.open(inputpath)
        
        image_tensor = transform(image)
    
        if torch.cuda.is_available():
            image_tensor = image_tensor.view(1, 3, 224, 224).cuda()
            #print("use cuda")
        else:
            image_tensor = image_tensor.view(1, 3, 224, 224)
            #print("use cuda")
        
        with torch.no_grad():
            self.model.eval()
            # Model outputs log probabilities
            out = self.model(image_tensor)

            confident = torch.exp(out)
            #print("confident of all class : ",confident[0].tolist())
            topk, topclass = confident.topk(1, dim=1)
            fileclass = self.document_class[topclass.cpu().numpy()[0][0]]
            #print("Output class :  ", document_class[topclass.cpu().numpy()[0][0]])
            #os.remove(inputpath) #ลบไฟล์รูปที่นำมาทำนายผล
            return confident,fileclass #รีเทิร์นค่าออกมาเป็น ค่า confident และ ผลของคลาสเอกสารที่ทำนายออกมา



#print(bieclass().predictIMG(r"E:\testpath\testfile\file_example_PNG_3MB.png"))