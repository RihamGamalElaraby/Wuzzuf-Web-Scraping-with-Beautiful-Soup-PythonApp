import csv
from itertools import zip_longest

import requests
from bs4 import BeautifulSoup

job_title = []
company_name = []
location_name = []
job_skill = []
result = requests.get("https://wuzzuf.net/search/jobs/?q=python&a=hpb")

src = result.content
#print (src)

soup = BeautifulSoup(src , "lxml")
#print(soup)

job_titles = soup.find_all("h2" , { "class" : "css-m604qf" })
#print(job_titles)
company_names = soup.find_all("a" , {"class" : "css-17s97q8" })
#print (company_names)
location_names = soup.find_all("span" , {"class" : "css-5wys0k"})
#print (location_names)
job_skills = soup.find_all("div"  , {"class" : "css-y4udm8"})
#print(job_skills)

for i in range (len(job_titles)):
    job_title.append(job_titles[i].text) 
    company_name.append(company_names[i].text)
    location_name.append(location_names[i].text)
    job_skill.append(job_skills[i].text)

print(job_title) 


with open("jobstest.csv" , "w") as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["Job title" , "Company name" , "Location" , "Slikks"])