import requests
import json

class Generator:
    def __init__(self, nutrition_input: list, ingredients: list = [], params: dict = {'n_neighbors': 5, 'return_distance': False}, is_diabetic: bool = False):
        self.nutrition_input = nutrition_input
        self.ingredients = ingredients
        self.params = params
        self.is_diabetic = is_diabetic

    def set_request(self, nutrition_input: list, ingredients: list, params: dict, is_diabetic: bool):
        self.nutrition_input = nutrition_input
        self.ingredients = ingredients
        self.params = params
        self.is_diabetic = is_diabetic

    def generate(self):
        request = {
            'nutrition_input': self.nutrition_input,
            'ingredients': self.ingredients,
            'params': self.params,
            'is_diabetic': self.is_diabetic
        }
        response = requests.post(
            url='http://localhost:8080/predict/', data=json.dumps(request))
        return response
