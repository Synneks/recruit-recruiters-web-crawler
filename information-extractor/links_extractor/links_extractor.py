from request_builder.requests_generator import RequestsGenerator
from request_sender.request_sender import RequestSender
from response_parser.response_parser import ResponseParser


class LinksExtractor:
    @staticmethod
    def extract_links_for_technology_and_location(technology, location):
        requests = RequestsGenerator.generate_requests(technology, location)
        responses = RequestSender.send_multiple_get_requests(requests)
        offer_links = ResponseParser.extract_from_multiple_responses(responses)
        return LinksExtractor.extract_technologies_from_offers(offer_links)

    @staticmethod
    def extract_technologies_from_offers(offer_links):
        ret_technologies = dict()
        for offer_link in offer_links:
            response = str(RequestSender.send_get_request(offer_link).content).lower()

            with open("technologies.txt", "r") as technologies:
                for technology in technologies.readlines():
                    technology = technology.strip("\n")
                    if response.find(technology.lower()) != -1:
                        if technology not in ret_technologies:
                            ret_technologies[technology] = 1
                        else:
                            ret_technologies[technology] += 1

        return ret_technologies

    @staticmethod
    def extract_links(location):
        links = dict()

        with open("technologies.txt", "r") as technologies:
            for technology in technologies.readlines():
                technology = technology.strip("\n")
                related_technologies = LinksExtractor.extract_links_for_technology_and_location(technology, location)
                total_offers = sum(related_technologies[key] for key in related_technologies)
                links[technology] = {"total_offers": total_offers, "technologies": related_technologies}

        return links
