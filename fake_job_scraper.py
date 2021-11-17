import requests
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")

"""
#printing all of the jobs
jobs = results.find_all("div", class_="card-content")
for job in jobs:
    title = job.find("h2", class_="title")
    company = job.find("h3", class_="company")
    location = job.find("p", class_="location")
    print(title.text.strip())
    print(company.text.strip())
    print(location.text.strip())
"""
python_jobs = results.find_all(
    "h2", string=lambda text: "python" in text.lower()
)

#print(python_jobs)
#print(len(python_jobs))

python_job_elements = [
    h2_element.parent.parent.parent for h2_element in python_jobs
]

for job in python_job_elements:
    title = job.find("h2", class_="title")
    company = job.find("h3", class_="company")
    location = job.find("p", class_="location")
    links = job.find_all("a")
    for link in links:
        link_url = link["href"]
        print(f"Apply here: {link_url}") if link.text == "Apply" else None
    print(title.text.strip())
    print(company.text.strip())
    print(location.text.strip())
