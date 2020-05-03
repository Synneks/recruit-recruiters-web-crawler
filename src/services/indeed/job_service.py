import requests
from bs4 import BeautifulSoup

from entities.JobOffer import JobOffer


class IndeedService:

    def __init__(self):
        self.site = "indeed"

    def get_job_offers(self, job_title, job_location, page_number):
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
            return self._create_job_offers(job_card_tags)

        except Exception as e:
            print("[ERROR] - Failed to get job offers from indeed.ro \n", e.args)
        return []

    def _create_job_offers(self, job_card_tags):
        job_offers = []
        for job_card_tag in job_card_tags:
            title_tag = job_card_tag.find("a")
            offer_link = "http://ro.indeed.com" + str(title_tag.attrs["href"])
            title = title_tag.get_text().strip()
            company_name = job_card_tag.find("span", {"class": "company"}).get_text().strip()
            description_page = self._get_description_page(offer_link)
            job_offer = JobOffer(title, company_name, self.site, offer_link)
            job_offer.application_link = self.get_application_link(description_page, offer_link)
            job_offer.location = job_card_tag.find("span", {"class": "location"}).get_text().strip()
            image_tag = description_page.find("img", {"class": "jobsearch-CompanyAvatar-image"})
            job_offer.company_image = image_tag.attrs["src"] if image_tag is not None else None
            job_offer.description = str(
                description_page.find("div", {"class": "jobsearch-jobDescriptionText"}))  # scrape html code
            work_type_tag = description_page.findAll("span",
                                                     {"class": "jobsearch-JobMetadataHeader-iconLabel"})
            job_offer.work_type = work_type_tag[1].get_text().strip() if len(work_type_tag) > 1 else None
            job_offers.append(job_offer)
        return job_offers

    def get_application_link(self, description_page, offer_link):
        button = description_page.find("a", {"class": "icl-Button"})
        return str(button.attrs["href"]) if \
            button.text == "Depuneți candidatura pe site-ul companiei" else offer_link

    @staticmethod
    def _get_description_page(job_card_link):
        page = requests.get(job_card_link)
        return BeautifulSoup(page.content, "html.parser")
