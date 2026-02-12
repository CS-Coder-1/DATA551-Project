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

