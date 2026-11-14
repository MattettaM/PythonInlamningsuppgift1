import random
from dataclasses import dataclass

@dataclass
class Person:
    '''
    Contains all values for a person from the dataset
    and functions for generating a random person
    '''

    age: int = 0
    sex: str = "Male"
    height: float = 100.
    weight: float = 50.
    systolic_bp: float = 100.
    cholesterol: float = 2.
    smoker: int = 0
    disease: int = 0

    def __str__(self):
        return f"Age: {self.age}\nSex: {self.sex}\nHeight: {self.height}\nWeight: {self.weight}\nBP: {self.systolic_bp}\nCholesterol: {self.cholesterol}\nSmoker: {self.smoker}\nDisease: {self.disease}"

    def generate_random_person(
            self,
            age_range: tuple[int, int],
            height_range: tuple[float, float],
            weight_range: tuple[float, float],
            bp_range: tuple[float, float],
            cholesterol_range: tuple[float, float],
            smoker_rate_by_gender: tuple[float, float],
            disease_rate: float
            ):
        '''
        Generates random values for the person
        based on values from the dataset

        age_range: Age from low to high

        height_range: Height from low to high

        weight_range: Weight from low to high

        bp_range: Blood pressure from low to high without decimals

        cholesterol_range: Cholesterol from low to high, without decimals

        smoker_rate_by_gender: Rate of how many are smokers by gender, male to female

        disease_rate: Rate of how many people in the data set have the disease
        '''

        self.age = random.randint(age_range[0], age_range[1])
        gender_int = random.randint(0, 1)
        self.sex = "Male" if gender_int == 0 else "Female"
        self.height = random.randint(int(height_range[0]), int(height_range[1]))
        self.weight = random.randint(int(weight_range[0]), int(weight_range[1]))
        self.systolic_bp = random.randint(int(bp_range[0]), int(bp_range[1]))
        self.cholesterol = random.randint(
            int(cholesterol_range[0]) * 100,
            int(cholesterol_range[1]) * 100) / 100
        self.smoker = int(random.randint(0, 100) < smoker_rate_by_gender[gender_int])
        self.disease = int(random.randint(0, 100) < disease_rate)
