Job Scraper Script
This repository contains a Python script for scraping job listings from the Wuzzuf job search website. The script is designed to extract details about job postings related to Python, including job title, company name, location, required skills, salary information, and job responsibilities.

Features
Job Title: Extracts the title of the job.
Company Name: Extracts the name of the company offering the job.
Location: Extracts the location where the job is based.
Skills Required: Extracts the skills required for the job.
Salary: Extracts the salary information if available.
Responsibilities: Extracts a summary of the job responsibilities.
Posting Date: Extracts the date when the job was posted.
Script Overview
Job Listing Extraction:

The script sends HTTP requests to the Wuzzuf job search page to retrieve job listings.
It iterates through pages to collect job titles, company names, locations, skills, and posting dates.
Detailed Job Information Extraction:

For each job listing, the script fetches the detailed job page to extract salary information and job responsibilities.
Data Export:

The collected data is saved into a CSV file named jobstest.csv.
Dependencies
requests: For sending HTTP requests.
beautifulsoup4: For parsing HTML content.
lxml: For HTML parsing.
