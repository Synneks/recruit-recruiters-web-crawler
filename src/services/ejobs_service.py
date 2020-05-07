import requests
from bs4 import BeautifulSoup

from entities.JobOffer import JobOffer

site = "ejobs"


def create_url(job_title, job_location, page_number):
    url = "https://www.ejobs.ro/locuri-de-munca/"
    if job_location is not None:
        url += f"{job_location}/"
    if page_number is not None:
        url = f"pagina{page_number}/"
    if job_title is not None:
        url += f"?cauta={job_title}"
    return url


def get_job_offers(job_title, job_location, page_number):
    try:
        url = create_url(job_title, job_location, page_number)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        job_list = soup.find(id="job-app-list")
        job_card_tags = job_list.findAll("div", {"class": "jobitem-inner"})
        return _create_job_offers(job_card_tags)
    except Exception as e:
        print("[ERROR] - Failed to get job offers from ejobs.ro \n", e.args)
    return []


def _create_job_offers(job_card_tags):
    job_offers = []
    for job_card_tag in job_card_tags:
        title_tag = job_card_tag.find("a", {"class": "title dataLayerItemLink"})
        title = title_tag.get_text().strip()
        company_name_tag = job_card_tag.find("h3", {"class": "jobitem-company"})
        company_name = company_name_tag.get_text().strip() if \
            company_name_tag is not None \
            else None
        offer_link = title_tag.attrs["href"]

        job_offer = JobOffer(title, company_name, "ejobs", offer_link)
        job_offer.application_link = _get_application_link(job_card_tag)
        job_offer.location = job_card_tag.find("span", {"class": "location-text"}).get_text().strip()
        image_tag = job_card_tag.find("img", {"class": "jobitem-logo-img"})
        job_offer.company_image = image_tag.attrs["data-src"] if \
            image_tag is not None \
            else None

        job_offers.append(job_offer)
    return job_offers


def get_job_details(job_offer):
    page = requests.get(job_offer.offer_link)
    soup = BeautifulSoup(page.content, "html.parser")
    job_offer.description = _get_job_criteria(soup) + _get_job_description(soup)
    job_offer.work_type = _get_work_type(soup)
    return job_offer


def _get_job_criteria(soup):
    h3_tags = []
    content_tags = []
    for criteria in soup.findAll("li", {"class": "Criteria__ListItem"}):
        h3_tags.append(criteria.find("h3", {"class": "Criteria__Title"}).get_text().strip())
        criteria_div = criteria.findAll("a", {"class": "Criteria__Link"})
        criteria_div.extend(criteria.findAll("span", {"class": "Criteria__Properties"}))
        content = ""
        for word in criteria_div:
            content += word.get_text() + ", "
        content_tags.append(content[:-2])

    criteria = "<ul> \n"
    for index in range(len(h3_tags)):
        criteria += f"<li> \n" \
                    f"<span><strong>{h3_tags[index].strip()}</strong> {content_tags[index].strip()}</span> \n" \
                    f"</li> \n"
    criteria += "</ul> \n"
    return criteria


def _get_job_description(soup):
    paragraphs = soup.findAll("div", {"class": "jobad-content-block"})
    full_description = ''
    for p in paragraphs:
        full_description += str(p)
    return full_description


def _get_application_link(job_card_tag):
    button_text = job_card_tag.find("a", {"class": "ebtn"})
    if button_text.attrs["title"] == "Aplică extern" or button_text.attrs["title"] == "Apply externally":
        return button_text.attrs["data-external-url"]
    else:
        title_tag = job_card_tag.find("a", {"class": "title dataLayerItemLink"})
        return title_tag.attrs["href"]


def _get_work_type(soup):
    work_type_tag = soup.find("div", {"id": "content-jobType"})
    return work_type_tag.find("a", {"class": "Criteria__Link"}).get_text().strip()
