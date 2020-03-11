import requests
from bs4 import BeautifulSoup

from entities.job_offers import JobOffer


def get_job_offers(job_title, job_location):
    try:
        url = f"https://www.hipo.ro/locuri-de-munca/cautajob/Toate-Domeniile/{job_location}/{job_title}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        job_rows = soup.find_all("tr", {"itemtype": "http://schema.org/JobPosting"})
        job_offers = create_job_offers(job_rows)
    except Exception  as e:
        print("[ERROR] - Failed to get job offers from hipo.ro \n", e.args)
    return job_offers


def create_job_offers(job_rows):
    job_offers = []
    for job_row in job_rows:
        title = job_row.find("span", {"itemprop": "title"}).get_text().strip()
        company_name = job_row.find("span", {"itemprop": "name"}).get_text().strip()
        application_url = "https://www.hipo.ro" + job_row.find("a", {"class": "job-title"})["href"]
        job_offer = JobOffer(title, company_name, application_url)
        job_offers.append(job_offer)
    return job_offers
