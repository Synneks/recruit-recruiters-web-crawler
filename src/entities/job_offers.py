class JobOffer:

    def __init__(self, job_title, company_name, application_link):
        self.__job_title = job_title
        self.__company_name = company_name
        self.__application_link = application_link

    def get_job_title(self):
        return self.__job_title

    def get_company_name(self):
        return self.__company_name

    def get_application_link(self):
        return self.__application_link

    def set_application_link(self, application_link):
        self.__application_link = application_link

    def __str__(self):
        return f"{self.__job_title} | {self.__company_name} | {self.__application_link}"

    def __repr__(self):
        return {"Job Title": self.__job_title,
                "Company Name": self.__company_name,
                "Application Link": self.__application_link}
