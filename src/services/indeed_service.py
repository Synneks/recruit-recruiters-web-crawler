import requests
from bs4 import BeautifulSoup

from entities.JobOffer import JobOffer
from exceptions import NoResultError

site = "indeed"


def create_url(job_title, job_location, page_number):
    if job_title is None and job_location is None:
        raise NoResultError
    url = "https://ro.indeed.com/jobs"
    job_title = "" if job_title is None else job_title.replace("-", "+")
    job_location = "" if job_location is None else job_location
    url += f"?q={job_title}&l={job_location}"

    if page_number is not None:
        page_number = (page_number - 1) * 10
        url += f"&start={page_number}"
    return url


def get_job_offers(job_title, job_location, page_number):
    try:
        url = create_url(job_title, job_location, page_number)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        job_card_tags = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        return _create_job_offers(job_card_tags)
    except NoResultError:
        print("[WARNING] Indeed needs job title and job location")
    except Exception as e:
        print("[ERROR] - Failed to get job offers from indeed.ro \n", e.args)
    return []


def _create_job_offers(job_card_tags):
    job_offers = []
    for job_card_tag in job_card_tags:
        title_tag = job_card_tag.find("a", {"data-tn-element": "jobTitle"})
        title = title_tag.get_text().strip()
        company_name = job_card_tag.find("span", {"class": "company"}).get_text().strip()
        offer_link = "http://ro.indeed.com" + str(title_tag.attrs["href"])
        description_page_soup = _get_soup_from_page(offer_link)
        job_offer = JobOffer(title, company_name, site, offer_link)
        job_offer.application_link = _get_best_application_link(description_page_soup, offer_link)
        location_tag = job_card_tag.find("span", {"class": "location"})
        job_offer.location = location_tag.get_text().strip() if location_tag is not None else None
        image_tag = description_page_soup.find("img", {"class": "jobsearch-CompanyAvatar-image"})
        job_offer.company_image = image_tag.attrs["src"] if \
            image_tag is not None \
            else None
        job_offers.append(job_offer)
    return job_offers


def _get_best_application_link(description_page, offer_link):
    button = description_page.find("a", {"class": "icl-Button"})
    return str(button.attrs["href"]) if \
        button.text == "Depuneți candidatura pe site-ul companiei" else offer_link


def _get_soup_from_page(job_card_link):
    page = requests.get(job_card_link)
    return BeautifulSoup(page.content, "html.parser")


def get_job_details(job_offer):
    soup = _get_soup_from_page(job_offer.offer_link)
    job_offer.description = str(
        soup.find("div", {"class": "jobsearch-jobDescriptionText"}))  # scrape html code
    work_type_tag = soup.findAll("span",
                                 {"class": "jobsearch-JobMetadataHeader-iconLabel"})
    job_offer.work_type = work_type_tag[1].get_text().strip() if \
        len(work_type_tag) > 1 \
        else None
    return job_offer
