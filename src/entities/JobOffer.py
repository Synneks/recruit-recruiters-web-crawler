class JobOffer:

    def __init__(self, job_title=None, company_name=None, site=None, offer_link=None):
        self.application_link = None
        self.company_image = None
        self.company_name = company_name
        self.description = None
        self.job_title = job_title
        self.location = None
        self.offer_link = offer_link
        self.site = site
        self.work_type = None

    def construct_from_json(self, json_string):
        self.application_link = json_string["applicationLink"]
        self.company_image = json_string["companyImage"]
        self.company_name = json_string["companyName"]
        self.description = json_string["description"] if json_string["description"] != "null" else None
        self.job_title = json_string["jobTitle"]
        self.location = json_string["location"]
        self.offer_link = json_string["offerLink"]
        self.site = json_string["site"]
        self.work_type = json_string["workType"] if json_string["workType"] != "null" else None
        return self
