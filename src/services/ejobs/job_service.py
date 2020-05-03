import requests
from bs4 import BeautifulSoup

from entities.JobOffer import JobOffer


class EjobsService:

    def __init__(self):
        self.site = "ejobs"

    def get_job_offers(self, job_title, job_location, page_number):
        try:
            if page_number > 0:
                url = f"https://www.ejobs.ro/locuri-de-munca/{job_location}/pagina{page_number}/?cauta={job_title}"
            else:
                url = f"https://www.ejobs.ro/locuri-de-munca/{job_location}/?cauta={job_title}"
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")

            job_list = soup.find(id="job-app-list")
            job_card_tags = job_list.find_all("div", {"class": "jobitem-inner"})
            return self._create_job_offers(job_card_tags)
        except Exception as e:
            print("[ERROR] - Failed to get job offers from ejobs.ro \n", e.args)
        return []

    def _create_job_offers(self, job_card_tags):
        job_offers = []
        for job_card_tag in job_card_tags:
            title_tag = job_card_tag.find("a", {"class": "title dataLayerItemLink"})
            title = title_tag.get_text().strip()
            company_name_tag = job_card_tag.find("h3", {"class": "jobitem-company"})
            company_name = company_name_tag.get_text().strip() if company_name_tag is not None else None
            offer_link = title_tag.attrs["href"]

            job_offer = JobOffer(title, company_name, "ejobs", offer_link)
            job_offer.application_link = self._get_application_link(job_card_tag)
            job_offer.location = job_card_tag.find("span", {"class": "location-text"}).get_text().strip()
            job_offer.company_image = job_card_tag.find("img", {"class": "jobitem-logo-img"}).attrs["data-src"]

            job_offers.append(job_offer)
        return job_offers

    def get_job_details(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        job_offer = JobOffer()
        job_offer.description = soup.find("div", {"class": "jobad-criteria"})
        job_offer.work_type = self._get_work_type(soup)
        return job_offer

    def _get_application_link(self, job_card_tag):
        button_text = job_card_tag.find("a", {"class": "ebtn"})
        if button_text.attrs["title"] == "Aplică extern":
            return button_text.attrs["data-external-url"]
        else:
            title_tag = job_card_tag.find("a", {"class": "title dataLayerItemLink"})
            return title_tag.attrs["href"]

    def _get_work_type(self, soup):
        work_type_tag = soup.find("div", {"id": "content-jobType"})
        return work_type_tag.find("a", {"class": "Criteria__Link"}).get_text().strip()
