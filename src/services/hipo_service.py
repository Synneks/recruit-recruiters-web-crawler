import requests
from bs4 import BeautifulSoup

from entities.JobOffer import JobOffer
from services import shared_service

site = "hipo"


def _create_url(job_title, job_location, page_number):
    url = "https://www.hipo.ro/locuri-de-munca/cautajob/Toate-Domeniile/"
    if job_location is not None:
        url += f"{job_location}/"
    else:
        url += "Toate-Orasele/"
    if job_title is not None:
        url += f"{job_title}/"
    if page_number is not None:
        url += f"{page_number}"
    return url


def get_job_offers(job_title, job_location, page_number):
    try:
        url = _create_url(job_title, job_location, page_number)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        job_rows = soup.find_all("tr", {"itemtype": "http://schema.org/JobPosting"})
        return _create_job_offers(job_rows)
    except Exception as e:
        print("[ERROR] - Failed to get job offers from hipo.ro \n", e.args)
        return []


def _create_job_offers(job_rows):
    job_offers = []
    try:
        for job_row in job_rows:
            title = job_row.find("span", {"itemprop": "title"}).get_text().strip()
            company_name = job_row.find("span", {"itemprop": "name"}).get_text().strip()
            offer_link = "https://www.hipo.ro" + job_row.find("a", {"class": "job-title"})["href"]
            job_offer = JobOffer(title, company_name, site, offer_link)
            job_offer.location = _get_locations(job_row)
            job_offer.work_type = job_row.find("span", {"itemprop": "employmentType"}).get_text().strip()
            job_offer.application_link = offer_link
            job_offers.append(job_offer)
    except Exception as e:
        shared_service.send_email(e)
    return job_offers


def _get_locations(job_row):
    locations_list = map(lambda location_tag: location_tag.get_text().strip(),
                         job_row.findAll("span", {"itemprop": "addressLocality"}))
    return ", ".join(map(str, locations_list))


def _get_description(soup):
    content = ""
    image_description = soup.find("div", {"id": "anunt-imagine"})
    if image_description is not None:
        content = str(image_description)
        content = content.replace("/public/resources", "https://hipo.ro/public/resources")

    description = soup.find("div", {"class": "content"})
    if description is None:
        description = soup.find("div", {"id": "anunt-content"})
        if description is None:
            return content
    description = str(description)
    content += description.replace("/public/resources", "https://hipo.ro/public/resources")
    return content


def _get_company_image(soup):
    company_image_div = soup.find("div", {"class": "companie-logo"})
    company_image_img = company_image_div.find("img")
    return company_image_img.attrs["src"] if \
        company_image_img is not None \
        else None


def get_job_details(job_offer):
    try:
        page = requests.get(job_offer.offer_link)
        soup = BeautifulSoup(page.content, "html.parser")
        job_offer.company_image = _get_company_image(soup)
        job_offer.description = _get_description(soup)
    except Exception as e:
        shared_service.send_email(e)
    return job_offer
