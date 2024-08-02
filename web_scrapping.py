import csv
from itertools import zip_longest

import requests
from bs4 import BeautifulSoup

# Initialize lists to store job details
job_title = []
company_name = []
location_name = []
job_skill = []
Links = []
salary = []
responsibilities = []
dated = []
page_number = 0

while True:
    # Send a request to the job search page
    result = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_number}")
    src = result.content

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(src, "lxml")

    # Find all the necessary job details
    job_titles = soup.find_all("h2", {"class": "css-m604qf"})
    company_names = soup.find_all("a", {"class": "css-17s97q8"})
    location_names = soup.find_all("span", {"class": "css-5wys0k"})
    job_skills = soup.find_all("div", {"class": "css-y4udm8"})
    posted_new = soup.find_all("div", {"class": "css-4c4ojb"})
    posted_old = soup.find_all("div", {"class": "css-do6t5g"})
    posted = [*posted_new, *posted_old]

    # If no job titles are found, break the loop
    if not job_titles:
        print("No more jobs found, ending scrape.")
        break

    # Ensure we have enough posted dates to match job titles
    if len(posted) < len(job_titles):
        posted.extend(["N/A"] * (len(job_titles) - len(posted)))

    # Iterate through the job titles and extract details
    for i in range(len(job_titles)):
        job_title.append(job_titles[i].text.strip())
        link = "https://wuzzuf.net" + job_titles[i].find("a").attrs['href']
        Links.append(link)
        company_name.append(company_names[i].text.strip())
        location_name.append(location_names[i].text.strip())
        job_skill.append(job_skills[i].text.strip())
        if isinstance(posted[i], str):
            dated.append(posted[i])
        else:
            dated.append(posted[i].text.strip())

    # Debugging print statements
    print(f"Processed page {page_number + 1}")
    print(f"Job titles so far: {len(job_title)}")
    print(f"Companies so far: {len(company_name)}")
    print(f"Locations so far: {len(location_name)}")
    print(f"Skills so far: {len(job_skill)}")
    print(f"Links so far: {len(Links)}")
    print(f"Dates so far: {len(dated)}")

    # Increment page number to move to the next page
    page_number += 1

# Extract additional details from individual job pages
for link in Links:
    try:
        result = requests.get(link)
        result.raise_for_status()  # Ensure we raise an exception for HTTP errors
        src = result.content
        soup = BeautifulSoup(src, "lxml")

        # Extract salary information
        salary_span = soup.find("span", {"class": "css-47jx3m"})
        if salary_span:
            salary.append(salary_span.text.strip())
        else:
            salary.append("N/A")

        # Extract job requirements
        requirements_section = soup.find("section", {"class": "css-ghicub"})
        if requirements_section:
            requirements = requirements_section.find_all("li")
            requirements_text = " | ".join([req.text.strip() for req in requirements])
            responsibilities.append(requirements_text)
        else:
            responsibilities.append("N/A")

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {link}: {e}")
        salary.append("N/A")
        responsibilities.append("N/A")

# Debugging prints to verify the scraped data
print("Final data collected:")
print(f"Job titles: {len(job_title)}")
print(f"Companies: {len(company_name)}")
print(f"Locations: {len(location_name)}")
print(f"Skills: {len(job_skill)}")
print(f"Links: {len(Links)}")
print(f"Salaries: {len(salary)}")
print(f"Responsibilities: {len(responsibilities)}")

# Export the scraped data to a CSV file
file_list = [job_title, company_name, dated, location_name, job_skill, Links, salary, responsibilities]
exported = zip_longest(*file_list)

with open("jobstest.csv", "w", newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["Job title", "Company name", "Date", "Location", "Skills", "Links", "Salary", "Responsibility"]) 
    wr.writerows(exported)
