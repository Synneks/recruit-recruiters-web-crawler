from time import time
from flask import Flask, jsonify, request
from flask_cors import CORS
import json

from services.ejobs import job_service as ejobs_job_service
from services.indeed import job_service as indeed_job_service
from services.hipo import job_service as hipo_job_service
from services import link_shortener

# creating the Flask application
app = Flask(__name__)
CORS(app)

@app.route("/jobs/<job_name>/<job_location>")
def get_jobs(job_name, job_location):
    print("[INFO] - Extracting ro.indeed.com offers...")
    start = time()
    indeed_offers = indeed_job_service.get_job_offers(job_name, job_location)
    end = time()
    print(f"[INFO] - Extracted {len(indeed_offers)} offers from ro.indeed.com in {end - start} seconds")

    print("[INFO] - Extracting ejobs.ro offers...")
    start = time()
    ejobs_offers = ejobs_job_service.get_job_offers(job_name, job_location)
    end = time()
    print(f"[INFO] - Extracted {len(ejobs_offers)} offers from ejobs.ro in {end - start} seconds")

    print("[INFO] - Extracting hipo.ro offers...")
    start = time()
    hipo_offers = hipo_job_service.get_job_offers(job_name, job_location)
    end = time()
    print(f"[INFO] - Extracted {len(hipo_offers)} offers from hipo.ro in {end - start} seconds")
    
    job_offers = indeed_offers + ejobs_offers + hipo_offers

    # print("[INFO] - Shortening links...")
    # job_offers = link_shortener.shorten(job_offers)

    return json.dumps(job_offers, default = lambda x: x.default(x))
    
 
if __name__ == '__main__':
    app.run(debug=True)