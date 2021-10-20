class ResponseParser:
    @staticmethod
    def parse_response(response):
        dict_content = response.json()
        return dict_content

    @staticmethod
    def extract_offer_links(response):
        ret_list = []

        for job_offer in ResponseParser.parse_response(response)['jobOffers']:
            ret_list.append(job_offer['offerLink'])

        return ret_list

    @staticmethod
    def extract_from_multiple_responses(responses):
        ret_list = []

        for response in responses:
            ret_list += ResponseParser.extract_offer_links(response)

        return ret_list
