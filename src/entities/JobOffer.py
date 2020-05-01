import json


class JobOffer(json.JSONEncoder):

    def __init__(self, job_title, company_name, site, application_link):
        self.job_title = job_title
        self.company_name = company_name
        self.site = site
        self.application_link = application_link

    def __str__(self):
        return f"{self.job_title} | {self.company_name} | {self.site} | {self.application_link}"

    def __repr__(self):
        return {"Job Title": self.job_title,
                "Company Name": self.company_name,
                "Site": self.site,
                "Application Link": self.application_link}

    def default(self, o):
        return {k.lstrip('_'): v for k, v in vars(o).items()}
