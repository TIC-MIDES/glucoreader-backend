from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory, APITestCase
from utils.helper_functions import recognize_digits, build_dict

class MeasureTest(APITestCase):

    def setUp(self):
        self.photos = [
            "https://lh3.googleusercontent.com/pw/ACtC-3eeqGBuuyePV3JGvw3S_MBRO5EtjBoazVxNNseU6pjQunRNF_2AVBUSGOatUZszocLUPQ2phD107EXVln5qn6GTlnqkr9P30aos24UEnb15tmTP-mzMG44Ex99DKHVHkUUCIeAkHyWAIySwkMdI7tDz0g=w490-h1007-no",
            "https://res.cloudinary.com/dobghm44l/image/upload/v1605553577/Measures/47976654/16-11-2020%2016:06:17:211892.png",
            # "https://res.cloudinary.com/dobghm44l/image/upload/v1605552208/Measures/47976654/16-11-2020%2015:43:28:648514.png",
            # "https://res.cloudinary.com/dobghm44l/image/upload/v1605552106/Measures/47976654/16-11-2020%2015:41:46:165034.png",
            # "https://res.cloudinary.com/dobghm44l/image/upload/v1605552010/Measures/47976654/16-11-2020%2015:40:10:608376.png",
            # "https://res.cloudinary.com/dobghm44l/image/upload/v1605556977/Measures/47976654/16-11-2020%2017:02:57:722117.png",
            # "http://res.cloudinary.com/dobghm44l/image/upload/v1605557558/Measures/47976654/16-11-2020%2017:12:38:643517.png",
            ]

    def test_new_measure(self):
        for photo in self.photos:
          results_list = recognize_digits(photo)
          values_dict = build_dict(results_list)
          print(values_dict)
