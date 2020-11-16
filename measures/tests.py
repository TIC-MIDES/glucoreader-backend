from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory, APITestCase
from utils.helper_functions import recognize_digits, build_dict

class MeasureTest(APITestCase):

    def setUp(self):
        self.photos = [
            "https://res.cloudinary.com/dobghm44l/image/upload/v1605553577/Measures/47976654/16-11-2020%2016:06:17:211892.png",
            "https://res.cloudinary.com/dobghm44l/image/upload/v1605552208/Measures/47976654/16-11-2020%2015:43:28:648514.png",
            "https://res.cloudinary.com/dobghm44l/image/upload/v1605552106/Measures/47976654/16-11-2020%2015:41:46:165034.png",
            "https://res.cloudinary.com/dobghm44l/image/upload/v1605552010/Measures/47976654/16-11-2020%2015:40:10:608376.png"]

    def test_new_measure(self):
        for photo in self.photos:
          results_list = recognize_digits(photo)
          values_dict = build_dict(results_list)
          print(values_dict)
