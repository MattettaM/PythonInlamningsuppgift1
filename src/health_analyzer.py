import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import src.io_functions as io_f
from src import viz
from src.person import Person
from src.viz import GraphTexts


class HealthAnalyzer:
    '''
    Class responsible for running correlation tests for cholesterol, blood pressure and smoking
    '''
    healthy_df: pd.DataFrame
    sick_df: pd.DataFrame
    healthy_rdf: pd.DataFrame
    sick_rdf: pd.DataFrame


    def __init__(self, df: pd.DataFrame):
        self.healthy_df = df[df["disease"] == 0].copy()
        self.sick_df = df[df["disease"] == 1].copy()

        random_people: list[Person] = []
        for _ in range(1000):
            person = Person(
            age=int(io_f.get_truncated_normal(
                df["age"].mean(), df["age"].std(), 18., 90.
            ).rvs()),
            height=np.random.normal(df["height"].mean(), df["height"].std()),
            weight=np.random.normal(df["weight"].mean(), df["weight"].std()),
            systolic_bp=np.random.normal(df["systolic_bp"].mean(), df["systolic_bp"].std()),
            cholesterol=np.random.normal(df["cholesterol"].mean(), df["cholesterol"].std()),
            smoker=int(np.random.rand() < df["smoker"].mean()),
            disease=int(np.random.rand() < df["disease"].mean())
        )
            random_people.append(person)
        random_set = pd.DataFrame([vars(person) for person in random_people])
        self.healthy_rdf = random_set[random_set["disease"] == 0].copy()
        self.sick_rdf = random_set[random_set["disease"] == 1].copy()


    def compare_disease_bp(self, bin_size: int = 20):
        '''
        Calculates the correlation between having the disease and higher blood pressure.
        Draws out histograms of the groupings, and prints out results of t-test, bootstrap, and normal approximation
        '''
        _, axs = plt.subplots(1, 2, figsize=(16, 6))

        viz.hist(
            axs[0],
            self.healthy_df["systolic_bp"],
            bin_size,
            GraphTexts(
                "Blood Pressure Grouping Data Set",
                "Blood Pressure",
                "Group Size"
            )
        )
        viz.hist(
            axs[0],
            self.sick_df["systolic_bp"],
            bin_size,
            color="red"
        )
        viz.add_normal_fit(axs[0], self.healthy_df["systolic_bp"], "purple", "Healthy", bin_size)
        viz.add_normal_fit(axs[0], self.sick_df["systolic_bp"], "orange", "Sick", bin_size)

        viz.hist(
            axs[1],
            self.healthy_rdf["systolic_bp"],
            bin_size,
            GraphTexts(
                "Blood Pressure Grouping Random Set",
                "Blood Pressure",
                "Group Size"
            ),
            labels="Healthy"
        )
        viz.hist(
            axs[1],
            self.sick_rdf["systolic_bp"],
            bin_size,
            color="red",
            labels="Sick"
        )
        viz.add_normal_fit(axs[1], self.healthy_rdf["systolic_bp"], "purple", "Healthy", bin_size)
        viz.add_normal_fit(axs[1], self.sick_rdf["systolic_bp"], "orange", "Sick", bin_size)

        plt.legend()
        plt.show()
        bp_t, bp_p = io_f.t_test(self.healthy_df["systolic_bp"], self.sick_df["systolic_bp"])
        bp_power = io_f.calc_power(self.healthy_df["systolic_bp"], self.sick_df["systolic_bp"])

        normal_approx_ci = io_f.normal_mean_ci(
            self.healthy_df["systolic_bp"], self.sick_df["systolic_bp"]
        )
        bp_obsdiff_s, bp_p_perm_s, bp_ci_s = io_f.bootstrap_ci(
	        self.healthy_df["systolic_bp"], self.sick_df["systolic_bp"], 1000
        )
        bp_obsdiff_l, bp_p_perm_l, bp_ci_l = io_f.bootstrap_ci(
	        self.healthy_df["systolic_bp"], self.sick_df["systolic_bp"], 10000
        )

        print(
f'''Normal Approximation Confidence Interval:   Low:{normal_approx_ci[0]}, High: {normal_approx_ci[1]}
Blood Pressure Bootstrap 1000:   Observed Diff: {bp_obsdiff_s}, P-Permutation: {bp_p_perm_s}, Confidence: {bp_ci_s[0]} : {bp_ci_s[1]}
Blood Pressure Bootstrap 10000:   Observed Diff: {bp_obsdiff_l}, P-Permutation: {bp_p_perm_l}, Confidence: {bp_ci_l[0]} : {bp_ci_l[1]}
Blood Pressure Correlation to Sickness:    t-score: {bp_t}, p-value: {bp_p}, power: {bp_power}''')


    def compare_disease_cholsterol(self, bin_size: int = 20):
        '''
        Calculates the correlation between having the disease and having higher cholesterol levels
        Draws histograms of the groupings, and prints out t-test results
        '''
        _, axs = plt.subplots(1, 2, figsize=(16, 6))

        viz.hist(
            axs[0],
            self.healthy_df["cholesterol"],
            bin_size,
            GraphTexts(
                "Cholesterol Grouping Data Set",
                "Cholesterol Levels",
                "Group Size"
            )
        )
        viz.hist(
            axs[0],
            self.sick_df["cholesterol"],
            bin_size,
            color="red"
        )
        viz.add_normal_fit(axs[0], self.healthy_df["cholesterol"], "purple", "Healthy", bin_size)
        viz.add_normal_fit(axs[0], self.sick_df["cholesterol"], "orange", "Sick", bin_size)

        viz.hist(
            axs[1],
            self.healthy_rdf["cholesterol"],
            bin_size,
            GraphTexts(
                "Cholesterol Grouping Random Set",
                "Cholesterol Levels",
                "Group Size"
            ),
            labels="Healthy"
        )
        viz.hist(
            axs[1],
            self.sick_rdf["cholesterol"],
            bin_size,
            color="red",
            labels="Sick"
        )
        viz.add_normal_fit(axs[1], self.healthy_rdf["cholesterol"], "purple", "Healthy", bin_size)
        viz.add_normal_fit(axs[1], self.sick_rdf["cholesterol"], "orange", "Sick", bin_size)

        plt.legend()
        plt.show()
        c_t, c_p = io_f.t_test(self.healthy_df["cholesterol"], self.sick_df["cholesterol"])
        print(f"Cholesterol Correlation to Sickness:  t-score:{c_t}, p-value:{c_p}")


    def draw_bp_correlation_scatters(self):
        '''
        Draws plots comparing bloodpressure with cholesterol and BMI
        '''
        _, axs = plt.subplots(1, 2, figsize=[16, 6])
        viz.scatter(
	        axs[0],
            self.healthy_df["cholesterol"],
            self.healthy_df["systolic_bp"],
            GraphTexts(
		        "Correlation of Cholesterol Levels and Blood Pressure",
                "Cholesterol Level (mmol/L)",
                "Blood Pressure (mmHg)"
            ),
            "blue",
            "purple",
            "Healthy",
            "Healthy Trend"
        )
        viz.scatter(
            axs[0],
            self.sick_df["cholesterol"],
            self.sick_df["systolic_bp"],
            dot_color="orange",
            trend_color = "red",
            label="Sick",
            trend_label="Sick Trend"
        )

        healthy_bmi = self.healthy_df["weight"] / ((self.healthy_df["height"] / 100) ** 2)
        sick_bmi = self.sick_df["weight"] / ((self.sick_df["height"] / 100) ** 2)
        viz.scatter(
	        axs[1],
            healthy_bmi,
            self.healthy_df["systolic_bp"],
            GraphTexts(
		        "Correlation of BMI and Blood Pressure",
                r"BMI (kg/m$^{2}$)",
                "Blood Pressure (mmHg)"
            ),
            "blue",
            "purple",
            "Healthy",
            "Healthy Trend"
        )
        viz.scatter(
            axs[1],
            sick_bmi,
            self.sick_df["systolic_bp"],
            dot_color="orange",
            trend_color="red",
            label="Sick",
            trend_label="Sick Trend"
        )
        plt.legend()
        plt.show()


    def print_values(self):
        '''Prints out the values of the data sets'''
        print(
f'''Data Set Sick Rate: {len(self.sick_df) / len(self.healthy_df) + len(self.sick_df)}
Random Set Sick Rate: {len(self.sick_rdf) / len(self.healthy_rdf) + len(self.sick_rdf)}
{"-" * 20}
Data Set Healthy Values
{io_f.get_composed_values(self.healthy_df)}
{"-" * 20}
Data Set Sick Values
{io_f.get_composed_values(self.sick_df)}
{"-" * 20}
Random Set Healthy Values
{io_f.get_composed_values(self.healthy_rdf)}
{"-" * 20}
Random Set Sick Values
{io_f.get_composed_values(self.sick_rdf)}''')
