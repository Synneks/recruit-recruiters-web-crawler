import requests
from bs4 import BeautifulSoup

from entities.job_offers import JobOffer


def get_job_offers(job_title, job_location, page_number):
    try:
        job_title = job_title.replace("-", "+")
        if page_number > 0:
            page_number = (page_number - 1) * 10
            url = f"https://ro.indeed.com/jobs?q={job_title}&l={job_location}&start={page_number}"
        else:
            url = f"https://ro.indeed.com/jobs?q={job_title}&l={job_location}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        job_card_tags = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        return create_job_offers(job_card_tags)
    except Exception as e:
        print("[ERROR] - Failed to get job offers from indeed.ro \n", e.args)
    return []


def create_job_offers(job_card_tags):
    job_offers = []
    for job_card_tag in job_card_tags:
        title_tag = job_card_tag.find("a")
        application_url = get_application_link(title_tag.attrs["href"])
        company_name = job_card_tag.find("span", {"class": "company"}).get_text().strip()
        title = title_tag.get_text().strip()
        job_offer = JobOffer(title, company_name, application_url)
        job_offers.append(job_offer)
    return job_offers


def get_application_link(job_card_link):
    job_card_link = "http://ro.indeed.com" + job_card_link
    page = requests.get(job_card_link)
    soup = BeautifulSoup(page.content, "html.parser")
    button = soup.find("a", {"class": "icl-Button"})
    if button.text == "Depuneți candidatura pe site-ul companiei":
        return button.attrs["href"]
    else:
        return job_card_link
