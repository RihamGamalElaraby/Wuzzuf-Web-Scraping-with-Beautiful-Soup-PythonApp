import csv
from itertools import zip_longest

import requests
from bs4 import BeautifulSoup


class JobScraper:
    def __init__(self, search_query, base_url, output_file):
        self.search_query = search_query
        self.base_url = base_url
        self.output_file = output_file
        self.job_title = []
        self.company_name = []
        self.location_name = []
        self.job_skill = []
        self.links = []
        self.salary = []
        self.responsibilities = []
        self.dated = []
        self.page_number = 0

    def fetch_page(self):
        url = f"{self.base_url}?a=hpb&q={self.search_query}&start={self.page_number}"
        result = requests.get(url)
        return BeautifulSoup(result.content, "lxml")

    def parse_job_details(self, soup):
        job_titles = soup.find_all("h2", {"class": "css-m604qf"})
        company_names = soup.find_all("a", {"class": "css-17s97q8"})
        location_names = soup.find_all("span", {"class": "css-5wys0k"})
        job_skills = soup.find_all("div", {"class": "css-y4udm8"})
        posted_new = soup.find_all("div", {"class": "css-4c4ojb"})
        posted_old = soup.find_all("div", {"class": "css-do6t5g"})
        posted = [*posted_new, *posted_old]

        if len(posted) < len(job_titles):
            posted.extend(["N/A"] * (len(job_titles) - len(posted)))

        for i in range(len(job_titles)):
            self.job_title.append(job_titles[i].text.strip())
            link = "https://wuzzuf.net" + job_titles[i].find("a").attrs['href']
            self.links.append(link)
            self.company_name.append(company_names[i].text.strip())
            self.location_name.append(location_names[i].text.strip())
            self.job_skill.append(job_skills[i].text.strip())
            self.dated.append(posted[i].text.strip() if not isinstance(posted[i], str) else posted[i])

    def fetch_job_details(self):
        for link in self.links:
            try:
                result = requests.get(link)
                result.raise_for_status()
                soup = BeautifulSoup(result.content, "lxml")
                
                salary_span = soup.find("span", {"class": "css-47jx3m"})
                self.salary.append(salary_span.text.strip() if salary_span else "N/A")

                requirements_section = soup.find("section", {"class": "css-ghicub"})
                if requirements_section:
                    requirements = requirements_section.find_all("li")
                    requirements_text = " | ".join([req.text.strip() for req in requirements])
                    self.responsibilities.append(requirements_text)
                else:
                    self.responsibilities.append("N/A")

            except requests.exceptions.RequestException as e:
                print(f"Failed to retrieve {link}: {e}")
                self.salary.append("N/A")
                self.responsibilities.append("N/A")

    def save_to_csv(self):
        file_list = [self.job_title, self.company_name, self.dated, self.location_name, self.job_skill, self.links, self.salary, self.responsibilities]
        exported = zip_longest(*file_list)

        with open(self.output_file, "w", newline='') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(["Job title", "Company name", "Date", "Location", "Skills", "Links", "Salary", "Responsibility"])
            wr.writerows(exported)

    def run(self):
        while True:
            soup = self.fetch_page()
            job_titles = soup.find_all("h2", {"class": "css-m604qf"})
            
            if not job_titles:
                print("No more jobs found, ending scrape.")
                break

            self.parse_job_details(soup)
            print(f"Processed page {self.page_number + 1}")
            print(f"Job titles so far: {len(self.job_title)}")
            print(f"Companies so far: {len(self.company_name)}")
            print(f"Locations so far: {len(self.location_name)}")
            print(f"Skills so far: {len(self.job_skill)}")
            print(f"Links so far: {len(self.links)}")
            print(f"Dates so far: {len(self.dated)}")
            
            self.page_number += 1
        
        self.fetch_job_details()
        self.save_to_csv()
        print("Scraping complete.")

# Example usage
if __name__ == "__main__":
    scraper = JobScraper(search_query="python", base_url="https://wuzzuf.net/search/jobs", output_file="jobstest.csv")
    scraper.run()
