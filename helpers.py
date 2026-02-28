import pandas as pd
import re
def job_type(title):
    title = str(title).lower()
    if "data scientist" in title or "data science" in title:
        return "Data Scientist"
    elif "data engineer" in title or "data engineering" in title:
        return "Data Engineer"
    elif "data analyst" in title or "data analysis" in title or "analyst" in title:
        return "Data Analyst"
    elif "machine learning scientist" in title or "machine learning science" in title:
        return "ML Scientist"
    elif "machine learning engineer" in title or "ml engineer" in title or "ml engineering" in title or "machine learning engineering" in title:
        return "ML Engineer"
    elif "ai engineer" in title or "ai engineering" in title:
        return "AI Engineer"
    elif "ai/ml engineer" in title or "ai/ml engineering" in title:
        return "AI/ML Engineer"
    elif "deep learning" in title:
        return "Deep Learning Engineer"
    elif "big data engineer" in title or "big data engineering" in title:
        return "Big Data Engineer"
    elif "analytics engineer" in title or "analytics engineering" in title:
        return "Analytics Engineer"
    elif "business analyst" in title or "business analysis" in title:
        return "Business Analyst"
    elif "bi analyst" in title or "business intelligence" in title or "bi analysis" in title or "business intelligence analysis" in title:
        return "Business Intelligence Analyst"
    elif "software engineer" in title or "software engineering" in title:
        return "Software Engineer"
    elif "data manager" in title or "manager" in title or "data management" in title or "management" in title:
        return "Data Manager"
    elif "cloud" in title:
        return "Cloud Engineer"
    elif "database" in title or "db" in title:
        return "Database Engineer"
    else:
        return "Other"


def extract_experience(description, title = ""):
    if pd.isna(description):
        return None
    description = description.lower()
    title = str(title).lower()
    #handle a range like 5-7 years
    range_match = re.search(r'\b(\d{1,2})\s*[-–]\s*(\d{1,2})\s*(?:years?|yrs?)\b', description)
    #average for ranges
    if range_match:
        low, high = int(range_match.group(1)), int(range_match.group(2))
        value = (low + high) / 2
    else:
        single_match = re.search(r'\b(\d{1,2})\+?\s*(?:years?|yrs?)\b', description)
        if single_match:
            value = float(single_match.group(1))
        else:
            return None
    return value

def company_size_clean(size):
    if pd.isna(size) or str(size).lower() == "decline to state":
        return None
    #remove commas
    size = str(size).lower().replace(",", "")
    if "-" in size:
        parts = size.split("-")
        low = int(parts[0])
        high = int(parts[1])
        return (low + high) / 2
    if "to" in size:
        parts = size.split(" to ")
        low = int(parts[0].strip())
        high = int(parts[1].strip())
        return (low + high) / 2
    if "+" in size:
        return int(size.replace("+", ""))
    try:
        return int(size)
    except:
        return None