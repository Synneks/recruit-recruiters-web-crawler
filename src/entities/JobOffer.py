import json
from json import JSONEncoder

import stringcase


class JobOffer(JSONEncoder):

    def __init__(self, job_title=None, company_name=None, site=None, offer_link=None):
        self.job_title = job_title
        self.company_name = company_name
        self.site = site
        self.offer_link = offer_link
        self.location = None
        self.company_image = None
        self.description = None
        self.work_type = None
        self.application_link = None

    def __sr__(self):
        return f"{self.job_title} | {self.company_name} | {self.site} | {self.offer_link} | {self.application_link}"

    def default(self, o):
        return {stringcase.camelcase(k): v for k, v in vars(o).items()}
