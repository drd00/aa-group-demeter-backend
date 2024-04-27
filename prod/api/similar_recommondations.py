from flask import Flask,jsonify, request
from flask_restful import Resource
import numpy as np
from api.security.verify_token import verify_token
from api.db.profile import get_profile

#Dummy data
existing_data = [
    {'uid': 97577, 'age': 30, 'bmi': 22, 'food_list': [{'food': 'Salmon Fillet', 'calories': 205, 'protein': 11.8, 'fat': 4.4, 'carbs': 3.3}]},
    {'uid': 23146, 'age': 23, 'bmi': 17, 'food_list': [{'food': 'Peanut butter', 'calories': 232, 'protein': 6.0, 'fat': 7.1, 'carbs': 19.9}]},
    {'uid': 14590, 'age': 50, 'bmi': 20, 'food_list': [{'food': 'Oatmeal', 'calories': 68, 'protein': 5.3, 'fat': 2.6, 'carbs': 27}]},
    {'uid': 52273, 'age': 40, 'bmi': 26, 'food_list': [{'food': 'Apple', 'calories': 122, 'protein': 14.9, 'fat': 2.8, 'carbs': 37.3}]},
    {'uid': 95805, 'age': 28, 'bmi': 23, 'food_list': [{'food': 'Banana', 'calories': 121, 'protein': 1.1, 'fat': 0.3, 'carbs': 23.0}]},
    {'uid': 11111, 'age': 35, 'bmi': 25, 'food_list': [{'food': 'Grilled Chicken Breast', 'calories': 165, 'protein': 31.0, 'fat': 3.6, 'carbs': 0}]},
    {'uid': 22222, 'age': 45, 'bmi': 30, 'food_list': [{'food': 'Quinoa', 'calories': 222, 'protein': 8.1, 'fat': 3.6, 'carbs': 39}]},
    {'uid': 33333, 'age': 20, 'bmi': 21, 'food_list': [{'food': 'Greek Yogurt', 'calories': 59, 'protein': 10.0, 'fat': 0.4, 'carbs': 3.6}]},
    {'uid': 44444, 'age': 55, 'bmi': 28, 'food_list': [{'food': 'Almonds', 'calories': 576, 'protein': 21.2, 'fat': 49.9, 'carbs': 21.6}]},
    {'uid': 55555, 'age': 25, 'bmi': 19, 'food_list': [{'food': 'Steamed Broccoli', 'calories': 55, 'protein': 3.7, 'fat': 0.6, 'carbs': 10.1}]},
    {'uid': 66666, 'age': 33, 'bmi': 24, 'food_list': [{'food': 'Cottage Cheese', 'calories': 104, 'protein': 11.1, 'fat': 4.3, 'carbs': 3.8}]},
    {'uid': 77777, 'age': 38, 'bmi': 27, 'food_list': [{'food': 'Brown Rice', 'calories': 112, 'protein': 2.6, 'fat': 0.9, 'carbs': 23.5}]},
    {'uid': 88888, 'age': 48, 'bmi': 29, 'food_list': [{'food': 'Avocado', 'calories': 160, 'protein': 2.0, 'fat': 14.7, 'carbs': 8.5}]},
    {'uid': 99999, 'age': 32, 'bmi': 18, 'food_list': [{'food': 'Eggs', 'calories': 155, 'protein': 12.6, 'fat': 10.6, 'carbs': 1.1}]},
    {'uid': 10101, 'age': 52, 'bmi': 23, 'food_list': [{'food': 'Whole Wheat Bread', 'calories': 68, 'protein': 3.6, 'fat': 0.9, 'carbs': 12.2}]},
    {'uid': 12121, 'age': 29, 'bmi': 26, 'food_list': [{'food': 'Tuna', 'calories': 179, 'protein': 39.3, 'fat': 1.0, 'carbs': 0}]},
    {'uid': 13131, 'age': 43, 'bmi': 21, 'food_list': [{'food': 'Kale', 'calories': 33, 'protein': 2.9, 'fat': 0.6, 'carbs': 6.7}]},
    {'uid': 14141, 'age': 34, 'bmi': 22, 'food_list': [{'food': 'Sweet Potato', 'calories': 86, 'protein': 1.6, 'fat': 0.1, 'carbs': 20.1}]},
    {'uid': 15151, 'age': 49, 'bmi': 24, 'food_list': [{'food': 'Lean Beef', 'calories': 250, 'protein': 26.0, 'fat': 15.0, 'carbs': 0}]},
    {'uid': 16161, 'age': 27, 'bmi': 20, 'food_list': [{'food': 'Spinach', 'calories': 23, 'protein': 2.9, 'fat': 0.4, 'carbs': 3.6}]},
    {'uid': 17171, 'age': 37, 'bmi': 25, 'food_list': [{'food': 'Chickpeas', 'calories': 269, 'protein': 14.5, 'fat': 4.2, 'carbs': 44.9}]},
    {'uid': 18181, 'age': 53, 'bmi': 19, 'food_list': [{'food': 'Salad Greens', 'calories': 15, 'protein': 1.3, 'fat': 0.2, 'carbs': 2.7}]},
    {'uid': 19191, 'age': 26, 'bmi': 18, 'food_list': [{'food': 'Cauliflower', 'calories': 25, 'protein': 1.9, 'fat': 0.3, 'carbs': 5.3}]},
    {'uid': 20202, 'age': 44, 'bmi': 28, 'food_list': [{'food': 'Turkey Breast', 'calories': 135, 'protein': 30.0, 'fat': 1.3, 'carbs': 0}]},
    {'uid': 21212, 'age': 31, 'bmi': 27, 'food_list': [{'food': 'Walnuts', 'calories': 654, 'protein': 15.2, 'fat': 65.2, 'carbs': 13.7}]},
    {'uid': 23232, 'age': 39, 'bmi': 22, 'food_list': [{'food': 'Cottage Cheese', 'calories': 104, 'protein': 11.1, 'fat': 4.3, 'carbs': 3.8}]},
    {'uid': 24242, 'age': 47, 'bmi': 26, 'food_list': [{'food': 'Quinoa', 'calories': 222, 'protein': 8.1, 'fat': 3.6, 'carbs': 39}]},
    {'uid': 25252, 'age': 24, 'bmi': 21, 'food_list': [{'food': 'Greek Yogurt', 'calories': 59, 'protein': 10.0, 'fat': 0.4, 'carbs': 3.6}]},
    {'uid': 26262, 'age': 36, 'bmi': 29, 'food_list': [{'food': 'Almonds', 'calories': 576, 'protein': 21.2, 'fat': 49.9, 'carbs': 21.6}]},
    {'uid': 27272, 'age': 51, 'bmi': 24, 'food_list': [{'food': 'Steamed Broccoli', 'calories': 55, 'protein': 3.7, 'fat': 0.6, 'carbs': 10.1}]},
    {'uid': 28282, 'age': 28, 'bmi': 23, 'food_list': [{'food': 'Cottage Cheese', 'calories': 104, 'protein': 11.1, 'fat': 4.3, 'carbs': 3.8}]},
    {'uid': 29292, 'age': 42, 'bmi': 27, 'food_list': [{'food': 'Brown Rice', 'calories': 112, 'protein': 2.6, 'fat': 0.9, 'carbs': 23.5}]},
    {'uid': 30303, 'age': 29, 'bmi': 29, 'food_list': [{'food': 'Avocado', 'calories': 160, 'protein': 2.0, 'fat': 14.7, 'carbs': 8.5}]},
    {'uid': 31313, 'age': 54, 'bmi': 25, 'food_list': [{'food': 'Eggs', 'calories': 155, 'protein': 12.6, 'fat': 10.6, 'carbs': 1.1}]},
    {'uid': 32323, 'age': 30, 'bmi': 22, 'food_list': [{'food': 'Whole Wheat Bread', 'calories': 68, 'protein': 3.6, 'fat': 0.9, 'carbs': 12.2}]},
    {'uid': 33333, 'age': 31, 'bmi': 26, 'food_list': [{'food': 'Tuna', 'calories': 179, 'protein': 39.3, 'fat': 1.0, 'carbs': 0}]},
    {'uid': 34343, 'age': 56, 'bmi': 30, 'food_list': [{'food': 'Kale', 'calories': 33, 'protein': 2.9, 'fat': 0.6, 'carbs': 6.7}]},
    {'uid': 35353, 'age': 26, 'bmi': 20, 'food_list': [{'food': 'Sweet Potato', 'calories': 86, 'protein': 1.6, 'fat': 0.1, 'carbs': 20.1}]},
    {'uid': 36363, 'age': 50, 'bmi': 24, 'food_list': [{'food': 'Lean Beef', 'calories': 250, 'protein': 26.0, 'fat': 15.0, 'carbs': 0}]},
    {'uid': 37373, 'age': 40, 'bmi': 25, 'food_list': [{'food': 'Spinach', 'calories': 23, 'protein': 2.9, 'fat': 0.4, 'carbs': 3.6}]},
    {'uid': 38383, 'age': 27, 'bmi': 27, 'food_list': [{'food': 'Chickpeas', 'calories': 269, 'protein': 14.5, 'fat': 4.2, 'carbs': 44.9}]},
    {'uid': 39393, 'age': 46, 'bmi': 19, 'food_list': [{'food': 'Salad Greens', 'calories': 15, 'protein': 1.3, 'fat': 0.2, 'carbs': 2.7}]},
    {'uid': 40404, 'age': 28, 'bmi': 18, 'food_list': [{'food': 'Cauliflower', 'calories': 25, 'protein': 1.9, 'fat': 0.3, 'carbs': 5.3}]},
    {'uid': 41414, 'age': 32, 'bmi': 28, 'food_list': [{'food': 'Turkey Breast', 'calories': 135, 'protein': 30.0, 'fat': 1.3, 'carbs': 0}]},
    {'uid': 42424, 'age': 52, 'bmi': 22, 'food_list': [{'food': 'Walnuts', 'calories': 654, 'protein': 15.2, 'fat': 65.2, 'carbs': 13.7}]},
    {'uid': 43434, 'age': 38, 'bmi': 26, 'food_list': [{'food': 'Cottage Cheese', 'calories': 104, 'protein': 11.1, 'fat': 4.3, 'carbs': 3.8}]},
    {'uid': 44444, 'age': 47, 'bmi': 23, 'food_list': [{'food': 'Quinoa', 'calories': 222, 'protein': 8.1, 'fat': 3.6, 'carbs': 39}]},
    {'uid': 45454, 'age': 25, 'bmi': 20, 'food_list': [{'food': 'Greek Yogurt', 'calories': 59, 'protein': 10.0, 'fat': 0.4, 'carbs': 3.6}]},
    {'uid': 46464, 'age': 37, 'bmi': 29, 'food_list': [{'food': 'Almonds', 'calories': 576, 'protein': 21.2, 'fat': 49.9, 'carbs': 21.6}]},
    {'uid': 47474, 'age': 53, 'bmi': 24, 'food_list': [{'food': 'Steamed Broccoli', 'calories': 55, 'protein': 3.7, 'fat': 0.6, 'carbs': 10.1}]},
    {'uid': 48484, 'age': 29, 'bmi': 22, 'food_list': [{'food': 'Cottage Cheese', 'calories': 104, 'protein': 11.1, 'fat': 4.3, 'carbs': 3.8}]},
    {'uid': 49494, 'age': 44, 'bmi': 27, 'food_list': [{'food': 'Brown Rice', 'calories': 112, 'protein': 2.6, 'fat': 0.9, 'carbs': 23.5}]},
    {'uid': 50505, 'age': 30, 'bmi': 29, 'food_list': [{'food': 'Avocado', 'calories': 160, 'protein': 2.0, 'fat': 14.7, 'carbs': 8.5}]},
    {'uid': 51515, 'age': 54, 'bmi': 25, 'food_list': [{'food': 'Eggs', 'calories': 155, 'protein': 12.6, 'fat': 10.6, 'carbs': 1.1}]},
    {'uid': 52525, 'age': 31, 'bmi': 26, 'food_list': [{'food': 'Whole Wheat Bread', 'calories': 68, 'protein': 3.6, 'fat': 0.9, 'carbs': 12.2}]},
    {'uid': 53535, 'age': 45, 'bmi': 27, 'food_list': [{'food': 'Tuna', 'calories': 179, 'protein': 39.3, 'fat': 1.0, 'carbs': 0}]},
    {'uid': 54545, 'age': 56, 'bmi': 30, 'food_list': [{'food': 'Kale', 'calories': 33, 'protein': 2.9, 'fat': 0.6, 'carbs': 6.7}]},
    {'uid': 55555, 'age': 27, 'bmi': 20, 'food_list': [{'food': 'Sweet Potato', 'calories': 86, 'protein': 1.6, 'fat': 0.1, 'carbs': 20.1}]},
    {'uid': 56565, 'age': 51, 'bmi': 24, 'food_list': [{'food': 'Lean Beef', 'calories': 250, 'protein': 26.0, 'fat': 15.0, 'carbs': 0}]},
    {'uid': 57575, 'age': 41, 'bmi': 25, 'food_list': [{'food': 'Spinach', 'calories': 23, 'protein': 2.9, 'fat': 0.4, 'carbs': 3.6}]},
    {'uid': 58585, 'age': 28, 'bmi': 27, 'food_list': [{'food': 'Chickpeas', 'calories': 269, 'protein': 14.5, 'fat': 4.2, 'carbs': 44.9}]},
    {'uid': 59595, 'age': 47, 'bmi': 19, 'food_list': [{'food': 'Salad Greens', 'calories': 15, 'protein': 1.3, 'fat': 0.2, 'carbs': 2.7}]},
    {'uid': 60606, 'age': 29, 'bmi': 18, 'food_list': [{'food': 'Cauliflower', 'calories': 25, 'protein': 1.9, 'fat': 0.3, 'carbs': 5.3}]},
    {'uid': 61616, 'age': 43, 'bmi': 28, 'food_list': [{'food': 'Turkey Breast', 'calories': 135, 'protein': 30.0, 'fat': 1.3, 'carbs': 0}]},
    {'uid': 62626, 'age': 52, 'bmi': 22, 'food_list': [{'food': 'Walnuts', 'calories': 654, 'protein': 15.2, 'fat': 65.2, 'carbs': 13.7}]},
    {'uid': 63636, 'age': 39, 'bmi': 26, 'food_list': [{'food': 'Cottage Cheese', 'calories': 104, 'protein': 11.1, 'fat': 4.3, 'carbs': 3.8}]},
    {'uid': 64646, 'age': 48, 'bmi': 23, 'food_list': [{'food': 'Quinoa', 'calories': 222, 'protein': 8.1, 'fat': 3.6, 'carbs': 39}]},
    {'uid': 65656, 'age': 24, 'bmi': 21, 'food_list': [{'food': 'Greek Yogurt', 'calories': 59, 'protein': 10.0, 'fat': 0.4, 'carbs': 3.6}]},
    {'uid': 66666, 'age': 36, 'bmi': 29, 'food_list': [{'food': 'Almonds', 'calories': 576, 'protein': 21.2, 'fat': 49.9, 'carbs': 21.6}]},
    {'uid': 67676, 'age': 53, 'bmi': 24, 'food_list': [{'food': 'Steamed Broccoli', 'calories': 55, 'protein': 3.7, 'fat': 0.6, 'carbs': 10.1}]},
    {'uid': 68686, 'age': 29, 'bmi': 22, 'food_list': [{'food': 'Cottage Cheese', 'calories': 104, 'protein': 11.1, 'fat': 4.3, 'carbs': 3.8}]},
    {'uid': 69696, 'age': 44, 'bmi': 27, 'food_list': [{'food': 'Brown Rice', 'calories': 112, 'protein': 2.6, 'fat': 0.9, 'carbs': 23.5}]},
    {'uid': 70707, 'age': 30, 'bmi': 29, 'food_list': [{'food': 'Avocado', 'calories': 160, 'protein': 2.0, 'fat': 14.7, 'carbs': 8.5}]},
    {'uid': 71717, 'age': 54, 'bmi': 25, 'food_list': [{'food': 'Eggs', 'calories': 155, 'protein': 12.6, 'fat': 10.6, 'carbs': 1.1}]},
    {'uid': 72727, 'age': 31, 'bmi': 26, 'food_list': [{'food': 'Whole Wheat Bread', 'calories': 68, 'protein': 3.6, 'fat': 0.9, 'carbs': 12.2}]},
    {'uid': 73737, 'age': 45, 'bmi': 27, 'food_list': [{'food': 'Tuna', 'calories': 179, 'protein': 39.3, 'fat': 1.0, 'carbs': 0}]},
    {'uid': 74747, 'age': 56, 'bmi': 30, 'food_list': [{'food': 'Kale', 'calories': 33, 'protein': 2.9, 'fat': 0.6, 'carbs': 6.7}]},
    {'uid': 75757, 'age': 27, 'bmi': 20, 'food_list': [{'food': 'Sweet Potato', 'calories': 86, 'protein': 1.6, 'fat': 0.1, 'carbs': 20.1}]},
    {'uid': 76767, 'age': 51, 'bmi': 24, 'food_list': [{'food': 'Lean Beef', 'calories': 250, 'protein': 26.0, 'fat': 15.0, 'carbs': 0}]},
    {'uid': 77777, 'age': 41, 'bmi': 25, 'food_list': [{'food': 'Spinach', 'calories': 23, 'protein': 2.9, 'fat': 0.4, 'carbs': 3.6}]},
    {'uid': 78787, 'age': 28, 'bmi': 27, 'food_list': [{'food': 'Chickpeas', 'calories': 269, 'protein': 14.5, 'fat': 4.2, 'carbs': 44.9}]},
    {'uid': 79797, 'age': 47, 'bmi': 19, 'food_list': [{'food': 'Salad Greens', 'calories': 15, 'protein': 1.3, 'fat': 0.2, 'carbs': 2.7}]},
    {'uid': 80808, 'age': 29, 'bmi': 18, 'food_list': [{'food': 'Cauliflower', 'calories': 25, 'protein': 1.9, 'fat': 0.3, 'carbs': 5.3}]},
    {'uid': 81818, 'age': 43, 'bmi': 28, 'food_list': [{'food': 'Turkey Breast', 'calories': 135, 'protein': 30.0, 'fat': 1.3, 'carbs': 0}]},
    {'uid': 82828, 'age': 52, 'bmi': 22, 'food_list': [{'food': 'Walnuts', 'calories': 654, 'protein': 15.2, 'fat': 65.2, 'carbs': 13.7}]},
    {'uid': 83838, 'age': 39, 'bmi': 26, 'food_list': [{'food': 'Cottage Cheese', 'calories': 104, 'protein': 11.1, 'fat': 4.3, 'carbs': 3.8}]},
    {'uid': 84848, 'age': 48, 'bmi': 23, 'food_list': [{'food': 'Quinoa', 'calories': 222, 'protein': 8.1, 'fat': 3.6, 'carbs': 39}]},
    {'uid': 85858, 'age': 24, 'bmi': 21, 'food_list': [{'food': 'Greek Yogurt', 'calories': 59, 'protein': 10.0, 'fat': 0.4, 'carbs': 3.6}]},
    {'uid': 86868, 'age': 36, 'bmi': 29, 'food_list': [{'food': 'Almonds', 'calories': 576, 'protein': 21.2, 'fat': 49.9, 'carbs': 21.6}]},
    {'uid': 87878, 'age': 53, 'bmi': 24, 'food_list': [{'food': 'Steamed Broccoli', 'calories': 55, 'protein': 3.7, 'fat': 0.6, 'carbs': 10.1}]},
    {'uid': 88888, 'age': 29, 'bmi': 22, 'food_list': [{'food': 'Cottage Cheese', 'calories': 104, 'protein': 11.1, 'fat': 4.3, 'carbs': 3.8}]},
    {'uid': 89898, 'age': 44, 'bmi': 27, 'food_list': [{'food': 'Brown Rice', 'calories': 112, 'protein': 2.6, 'fat': 0.9, 'carbs': 23.5}]},
    {'uid': 90909, 'age': 30, 'bmi': 29, 'food_list': [{'food': 'Avocado', 'calories': 160, 'protein': 2.0, 'fat': 14.7, 'carbs': 8.5}]},
    {'uid': 91919, 'age': 54, 'bmi': 25, 'food_list': [{'food': 'Eggs', 'calories': 155, 'protein': 12.6, 'fat': 10.6, 'carbs': 1.1}]},
    {'uid': 92929, 'age': 31, 'bmi': 26, 'food_list': [{'food': 'Whole Wheat Bread', 'calories': 68, 'protein': 3.6, 'fat': 0.9, 'carbs': 12.2}]},
    {'uid': 93939, 'age': 45, 'bmi': 27, 'food_list': [{'food': 'Tuna', 'calories': 179, 'protein': 39.3, 'fat': 1.0, 'carbs': 0}]},
    {'uid': 94949, 'age': 56, 'bmi': 30, 'food_list': [{'food': 'Kale', 'calories': 33, 'protein': 2.9, 'fat': 0.6, 'carbs': 6.7}]},
    {'uid': 95959, 'age': 27, 'bmi': 20, 'food_list': [{'food': 'Sweet Potato', 'calories': 86, 'protein': 1.6, 'fat': 0.1, 'carbs': 20.1}]},
    {'uid': 96969, 'age': 51, 'bmi': 24, 'food_list': [{'food': 'Lean Beef', 'calories': 250, 'protein': 26.0, 'fat': 15.0, 'carbs': 0}]},
    {'uid': 97979, 'age': 41, 'bmi': 25, 'food_list': [{'food': 'Spinach', 'calories': 23, 'protein': 2.9, 'fat': 0.4, 'carbs': 3.6}]},
    {'uid': 98989, 'age': 28, 'bmi': 27, 'food_list': [{'food': 'Chickpeas', 'calories': 269, 'protein': 14.5, 'fat': 4.2, 'carbs': 44.9}]},
    {'uid': 99999, 'age': 47, 'bmi': 19, 'food_list': [{'food': 'Salad Greens', 'calories': 15, 'protein': 1.3, 'fat': 0.2, 'carbs': 2.7}]}
]


class FoodPreference(Resource):
    method_decorators = [verify_token]  # Apply the token verification decorator to all methods

    def get(self,**kwargs):
        uid = kwargs.get('user_id')
        profile = get_profile(uid)
        bmi_w = self.return_bmi(profile['weight'], profile['height'])
        age = profile['age']
        food_preference = self.get_food_preference( age, bmi_w)
        food_preference_serializable = {
            'food_list': [{
                'food': item['food'],
                'calories': item['calories'],
                'protein': item['protein'],
                'fat': item['fat'],
                'carbs': item['carbs']
            } for item in food_preference]
        }
        return food_preference_serializable


    def get_food_preference(self, age, bmi):
        age_bmi_data = np.array([(data['age'], data['bmi']) for data in existing_data])
        new_data = np.array([age, bmi])
        distances = np.linalg.norm(age_bmi_data - new_data, axis=1)
        closest_index = np.argmin(distances)
        closest_array = existing_data[closest_index]
        return closest_array['food_list']
    
    def return_bmi(self,weight, height):
        bmi = float(weight) / (float(height) * float(height))

        return bmi