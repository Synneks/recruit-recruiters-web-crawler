import json
from time import time

import stringcase
from flask import Flask, request
from flask_cors import CORS
from werkzeug.exceptions import abort

from entities.JobOffer import JobOffer
from services.ejobs import job_service as ejobs_scrapper
from services.hipo import job_service as hipo_scrapper
from services.indeed import job_service as indeed_scrapper

app = Flask(__name__)
CORS(app)


@app.route("/jobs/<job_name>/<job_location>/<page_number>")
def get_jobs_from_page(job_name, job_location, page_number, methods=['PUT']):
    return scrape_jobs(job_name, job_location, page_number)


@app.route("/jobs/<job_name>/<job_location>")
def get_jobs(job_name, job_location):
    return scrape_jobs(job_name, job_location)


def scrape_jobs(job_name, job_location, page_number=0):
    page_number = int(page_number)
    print("[INFO] - Extracting ro.indeed.com offers...")
    start = time()
    indeed_offers = indeed_scrapper.get_job_offers(job_name, job_location, page_number)
    end = time()
    print(f"[INFO] - Extracted {len(indeed_offers)} offers from ro.indeed.com in {end - start} seconds")

    print("[INFO] - Extracting ejobs.ro offers...")
    start = time()
    ejobs_offers = ejobs_scrapper.get_job_offers(job_name, job_location, page_number)
    end = time()
    print(f"[INFO] - Extracted {len(ejobs_offers)} offers from ejobs.ro in {end - start} seconds")

    print("[INFO] - Extracting hipo.ro offers...")
    start = time()
    hipo_offers = hipo_scrapper.get_job_offers(job_name, job_location, page_number)
    end = time()
    print(f"[INFO] - Extracted {len(hipo_offers)} offers from hipo.ro in {end - start} seconds")

    job_offers = indeed_offers + ejobs_offers + hipo_offers
    return json.dumps(job_offers, indent=2, sort_keys=True, default=lambda x: default(x))


@app.route("/job/details", methods=['PUT'])
def get_job_description():
    job_offer = None
    try:
        job_offer = JobOffer()
        job_offer.construct_from_json(request.json)
    except Exception as e:
        print(f"[WARNING] No valid body included in request", e.args)
        abort(400, "No valid body included")

    print(f"[INFO] - Gettting description from {job_offer.offer_link}")
    start = time()
    if job_offer.site == indeed_scrapper.site:
        job_offer = indeed_scrapper.get_job_details(job_offer)
    elif job_offer.site == ejobs_scrapper.site:
        job_offer = ejobs_scrapper.get_job_details(job_offer)
    elif job_offer.site == hipo_scrapper.site:
        job_offer = hipo_scrapper.get_job_details(job_offer)
    else:
        print(f"[WARNING] Unavailable scrapper for url: {job_offer.offer_link}")
        abort(501, f"Scrapper unavailable for {job_offer.site} or link {job_offer.offer_link}")
    end = time()
    print(f"[INFO] - Scrape in {end - start} seconds")
    return json.dumps(default(job_offer), indent=2, sort_keys=True)


def default(o):
    return {stringcase.camelcase(k): v for k, v in vars(o).items()}


if __name__ == '__main__':
    app.run(debug=True)
