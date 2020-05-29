import json
from time import time
import dotenv
import os

from flask import Flask, request, url_for, render_template
from flask_cors import CORS
from werkzeug.exceptions import abort

from entities.JobOffer import JobOffer
from services import ejobs_service, hipo_service, indeed_service
from services import shared_service

app = Flask(__name__)
CORS(app)


@app.route("/")
def main_page():
    links = []
    for rule in app.url_map.iter_rules():
        if len(rule.defaults) >= len(rule.arguments):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return render_template("all_links.html", links=links)


@app.route("/jobs")
def scrape_jobs():
    job_title = request.args.get('title')
    job_location = request.args.get('location')
    page_number = request.args.get('page')
    page_number = shared_service.check_page_number(page_number)
    returned_json = {'indeed': {},
                     'ejobs': {},
                     'hipo': {}
                     }
    print("[INFO] - Extracting ro.indeed.com offers...")
    start = time()
    indeed_offers = indeed_service.get_job_offers(job_title, job_location, page_number)
    end = time()
    returned_json['indeed']['amount'] = len(indeed_offers)
    returned_json['indeed']['time'] = float("{:.2f}".format(end - start))
    print(f"[INFO] - Extracted {len(indeed_offers)} offers from ro.indeed.com in {end - start} seconds")

    print("[INFO] - Extracting ejobs.ro offers...")
    start = time()
    ejobs_offers = ejobs_service.get_job_offers(job_title, job_location, page_number)
    end = time()
    returned_json['ejobs']['amount'] = len(ejobs_offers)
    returned_json['ejobs']['time'] = float("{:.2f}".format(end - start))
    print(f"[INFO] - Extracted {len(ejobs_offers)} offers from ejobs.ro in {end - start} seconds")

    print("[INFO] - Extracting hipo.ro offers...")
    start = time()
    hipo_offers = hipo_service.get_job_offers(job_title, job_location, page_number)
    end = time()
    returned_json['hipo']['amount'] = len(hipo_offers)
    returned_json['hipo']['time'] = float("{:.2f}".format(end - start))
    print(f"[INFO] - Extracted {len(hipo_offers)} offers from hipo.ro in {end - start} seconds")

    job_offers = indeed_offers + ejobs_offers + hipo_offers

    returned_json['jobOffers'] = shared_service.serialize_list(job_offers)
    return returned_json


@app.route("/job/details", methods=['PUT'])
def get_job_description():
    job_offer = None
    try:
        job_offer = JobOffer()
        job_offer.construct_from_json(request.json)
    except Exception as e:
        print(f"[WARNING] No valid body included in request", e.args)
        abort(400, "No valid body included")

    print(f"[INFO] - Getting description from {job_offer.offer_link}")
    start = time()
    if job_offer.site == indeed_service.site:
        job_offer = indeed_service.get_job_details(job_offer)
    elif job_offer.site == ejobs_service.site:
        job_offer = ejobs_service.get_job_details(job_offer)
    elif job_offer.site == hipo_service.site:
        job_offer = hipo_service.get_job_details(job_offer)
    else:
        print(f"[WARNING] Unavailable scrapper for url: {job_offer.offer_link}")
        abort(501, f"Scrapper unavailable for {job_offer.site} or link {job_offer.offer_link}")
    end = time()
    print(f"[INFO] - Scrape in {end - start} seconds")
    return json.dumps(shared_service.to_json(job_offer), indent=2, sort_keys=True)


if __name__ == '__main__':
    print("Loading .env...")
    dotenv.load_dotenv()
    print(".env loaded")
    app.run(debug=True)
