from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from profile_details.models import *

from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO, BytesIO
import re

from rest_framework.parsers import MultiPartParser
from django.core.files.storage import FileSystemStorage
from rest_framework.exceptions import APIException

# Create your views here.
class CandidateProfileAddView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES['file']
        if str(file_obj).split('.')[-1]!='pdf':
            raise APIException({'status':0, 'msz':'Please upload a proper PDF file'})
        else:
            # print("file_obj",file_obj)
            
            fs = FileSystemStorage(location="media/profile_details")
            # print("fs",fs)
            filename = fs.save(file_obj.name, file_obj)
            file_url = "media/profile_details/"+filename
            # print("file_url",file_url,filename)

            # scrape = open("./my_cv_test.pdf", 'rb') # for local files
            scrape = open(file_url, 'rb') #for upload file Externally
            pdfFile = BytesIO(scrape.read())
            rsrcmgr = PDFResourceManager()
            retstr = StringIO()
            codec = 'utf-8'
            laparams = LAParams()
            device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

            interpreter = PDFPageInterpreter(rsrcmgr, device)
            password = ""
            maxpages = 0
            caching = True
            pagenos=set()
            for page in PDFPage.get_pages(pdfFile, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
                interpreter.process_page(page)

            device.close()
            textstr = retstr.getvalue()
            retstr.close()
            pdfFile.close()
            # print("textstr",textstr.splitlines())
            multiline = textstr.splitlines()


            name = None
            skills = None
            skill_list = []
            for line in multiline:
                # print(line)
                if (line.lower().find('name') == 0): #if name in first position 
                    if name is None:
                        name = re.sub('^[Nn][Aa][Mm][Ee][\s\W]+','',line) # Get only name
                        print("name",name)

                if (line.lower().find('skills') == 0) or (line.lower().find('skill') == 0):
                    if skills is None:
                        skills = re.sub('^\w+[\s\W]+','',line) # Get only name
                        if skills:
                            skill_list = skills.split(",")
                            print("skill_list",skill_list)

                if name and skills:
                    break

            emails = re.findall(r'[\w\.-]+@[\w\.]+', textstr)
            mob_no = re.findall(r'[6-9]\d{9}', textstr)
            print("emails",emails, mob_no)

            # print(outputString)

            crt_filter = {}
            if name:
                crt_filter['name'] = name
                if mob_no:
                    crt_filter['phone_no'] = mob_no[0]
                if emails:
                    crt_filter['email'] = emails[0]
                candidate_profile,created1 = CandidateDetails.objects.get_or_create(**crt_filter)
                print("candidate_profile",candidate_profile, created1)
                if candidate_profile and skill_list:
                    for i in skill_list:
                        skills_create, created2 = Skills.objects.get_or_create(candidate=candidate_profile,skill=i)
                        print("skills_create, created2",skills_create, created2)
    
                return Response({'result':{'request_status':1,'msg':'Successful'}})

            else:
                return Response({'result':{'request_status':0,'msg':'Failure'}})
