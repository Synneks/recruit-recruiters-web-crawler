from links_extractor.links_extractor import LinksExtractor
from request_builder.requests_generator import RequestsGenerator
from request_sender.request_sender import RequestSender
import json


def main():
    print(LinksExtractor.extract_links("Cluj-Napoca"))


if __name__ == "__main__":
    main()