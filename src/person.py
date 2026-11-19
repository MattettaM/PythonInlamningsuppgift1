from dataclasses import dataclass

import numpy as np


@dataclass
class Person:
    '''
    Contains all values for a person from the dataset
    and functions for generating a random person
    '''

    age: int
    height: float
    weight: float
    systolic_bp: float
    cholesterol: float
    smoker: int
    disease: int
    sex: str = "Male" if np.random.randint(0, 1) == 0 else "Female"

    def __str__(self):
        return f"Age: {self.age}\nSex: {self.sex}\nHeight: {self.height}\nWeight: {self.weight}\nBP: {self.systolic_bp}\nCholesterol: {self.cholesterol}\nSmoker: {self.smoker}\nDisease: {self.disease}"
