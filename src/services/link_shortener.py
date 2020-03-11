from pyshorteners import Shortener

def shorten(jobs_list):
    shortener = Shortener('Tinyurl', timeout= 9000)
    for job in jobs_list:
        shortened_link = shortener.short(job.get_application_link())
        job.set_application_link(shortened_link)
    return jobs_list