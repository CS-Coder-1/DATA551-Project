# Proposal

## 1. Motivation and Purpose

Our role: Future data scientists wanting to know where to find jobs and the average salaries for recent job postings

Target audience: Ourselves and anyone else looking for work in tech

Due to the high volume of postings and a large range of salaries, is quite difficult to navigate the current tech job market and find the job that is right for you (in terms of salary, location, etc.). To address this, we are building an interactive dashboard that allows users to explore the current tech job market through multi-dimensional filtering. Users can see the differences between job titles (e.g., Data Scientist vs. Data Analyst), locations, and companies to find information about their ideal job.

## 2. Description of the Data

The dataset is broken down into 5 smaller datasets: Cyber Security, Software Engineering, IT, Product Management, and Data Science, each with their own spreadsheet. We want to focus on the Data Science dataset that includes 8935 job postings from sites such as Indeed or Zip Recruiter. Each posting has 35 associated variables, but the ones we want to focus on are the site the posting was found on (`site`), the job title and type of job (`title`, `job_type`), the company (`company`), location (`location`), the salary range (`min_amount`, `max_amount`, `mean_salary`), the size of the company (`company_num_employees`). 

## 3. Research Questions and Usage Scenarios

### Research Question:

How does the salary range vary across different locations and job titles?

### Usage Scenario:

John is a new grad of a Data Science program and is starting his job search. He wants to explore a dataset to in order to compare the effect of different variables on potential salaries and identify the most relevant variables (experience level, company size, location, etc.) he should base his job search on. When John logs onto the job comparison app, he sees a comparison of the top 10 highest paying job titles, which helps him decide if he'd rather stick with "Data Science" roles exclusively or branch out to other specialties such as "Machine Learning" or "Data Analysis". He uses the interactive filters to see an overview of salary trends compared to company size, as he wants to work at a smaller company but still recieve fair compensation. To finalize where he should live, he also makes use of the job distribution map to see where relevant jobs are most concentrated. While doing this, he may notice that while big cities have some jobs with very high pay, mid-sized companies in smaller cities seem to offer more steady and predictable salaries for people just starting out. He then checks the boxplot of salary distributions for his experience level to ensure his expectations are realistic. Based on all of the new information he has collected, he decides to focus his seach on "Data Scientist" roles in mid-sized companies in smaller cities.
