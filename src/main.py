import json
from time import time

from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import abort

from services.ejobs.job_service import EjobsService
from services.hipo.job_service import HipoService
from services.indeed.job_service import IndeedService

app = Flask(__name__)
CORS(app)
indeed_service = IndeedService()
ejobs_service = EjobsService()
hipo_service = HipoService()


@app.route("/jobs/<job_name>/<job_location>/<page_number>")
def get_jobs(job_name, job_location, page_number):
    page_number = int(page_number)
    print("[INFO] - Extracting ro.indeed.com offers...")
    start = time()
    indeed_offers = indeed_service.get_job_offers(job_name, job_location, page_number)
    end = time()
    print(f"[INFO] - Extracted {len(indeed_offers)} offers from ro.indeed.com in {end - start} seconds")

    print("[INFO] - Extracting ejobs.ro offers...")
    start = time()
    ejobs_offers = ejobs_service.get_job_offers(job_name, job_location, page_number)
    end = time()
    print(f"[INFO] - Extracted {len(ejobs_offers)} offers from ejobs.ro in {end - start} seconds")

    print("[INFO] - Extracting hipo.ro offers...")
    start = time()
    hipo_offers = hipo_service.get_job_offers(job_name, job_location, page_number)
    end = time()
    print(f"[INFO] - Extracted {len(hipo_offers)} offers from hipo.ro in {end - start} seconds")

    job_offers = indeed_offers + ejobs_offers + hipo_offers
    return json.dumps(job_offers, indent=2, sort_keys=True, default=lambda x: x.default(x))


@app.route("/job/details/<site>/<url>")
def get_job_description(site, url):
    url = "https://www.ejobs.ro/user/locuri-de-munca/facility-manager/1286745"
    job_offer = None
    print(f"[INFO] - Gettting description from {url}")
    start = time()
    if site == indeed_service.site:
        job_offer = indeed_service.get_job_details(url)
    elif site == ejobs_service.site:
        job_offer = ejobs_service.get_job_details(url)
    elif site == hipo_service.site:
        job_offer = hipo_service.get_job_details(url)
    else:
        print(f"[WARNING] Unavailable scrapper for url: {url}")
        abort(501, f"Scrapper unavailable for {site} or link {url}")
    end = time()
    print(f"[INFO] - Scrape in {end - start} seconds")
    return json.dumps([job_offer], indent=2, sort_keys=True, default=lambda x: x.default(x))


if __name__ == '__main__':
    app.run(debug=True)
