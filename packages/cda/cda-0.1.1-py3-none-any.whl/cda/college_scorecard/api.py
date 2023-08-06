# Data source: College Scorecard
import ssl

import pandas as pd

from ._data_processing import DataProcessor, MisValueFiller


class Dataset:

    def __init__(self, path='https://raw.githubusercontent.com/alisoltanirad/'
                            'CDA/main/cda/college_scorecard/'
                            'college_scorecard.csv'):
        ssl._create_default_https_context = ssl._create_unverified_context
        self._dataset = pd.read_csv(path, dtype='unicode')
        self._data_processor = DataProcessor()
        self._mis_value_filler = MisValueFiller()
        self.college_names = self._dataset['instnm']
        self.ownership = self._data_processor._ownership_types(
            self._dataset['control']
        )


class CollegeData(Dataset):

    def __init__(self, path='https://raw.githubusercontent.com/alisoltanirad/'
                            'CDA/main/cda/college_scorecard/'
                            'college_scorecard.csv'):
        Dataset.__init__(self, path)
        self._set_general_info()
        self._set_fiscal_info()
        self._set_evaluation_metrics()

    def get_info(self):
        data = {
            'Name': self.college_names,
            'Ownership': self.ownership,
            'State': self.state,
            'Student_Size': self.student_size,
            'Is_Online_Only': self.online_only,
            'Is_Men_Only': self.men_only,
            'Is_Women_Only': self.women_only,
            'Is_Religious_Affiliate': self.religious_affiliate,
            'Is_For_Profit': self.for_profit,
            'Tuition_Revenue': self.tuition_revenue,
            'Instructional_Expenditure': self.instructional_expenditure,
            'Faculty_Salary': self.faculty_salary,
            'Faculty_Full_Time_Rate': self.faculty_fulltime_rate,
            'Highest_Degree': self.highest_degrees,
        }
        return pd.DataFrame(data)

    def get_evaluation_metrics(self):
        data = {
            'Name': self.college_names,
            'Admission_Rate': self.admission_rates,
            'Completion_Rate_Overall': self.completion_rate_avg,
            'SAT_Scores_Overall': self.sat_scores,
        }
        return pd.DataFrame(data)

    def _set_general_info(self):
        self.state = self._dataset['stabbr']
        self.student_size = self._mis_value_filler.mean(
            self._dataset['ugds'], int
        )
        self.online_only = self._dataset['distanceonly'].fillna('false')
        self.men_only = self._dataset['menonly'].fillna('false')
        self.women_only = self._dataset['womenonly'].fillna('false')
        self.religious_affiliate = self._data_processor._is_religious_affiliate(
            self._dataset['relaffil']
        )
        self.for_profit = self._data_processor._is_for_profit(
            self._dataset['control']
        )
        self.highest_degrees = self._data_processor._degree_types(
            self._dataset['highdeg']
        )

    def _set_fiscal_info(self):
        self.tuition_revenue = self._mis_value_filler.mean(
            self._dataset['tuitfte'], int
        )
        self.instructional_expenditure = self._mis_value_filler.mean(
            self._dataset['inexpfte'], int
        )
        self.faculty_salary = self._mis_value_filler.mean(
            self._dataset['avgfacsal'], int
        )
        self.faculty_fulltime_rate = self._mis_value_filler.mean(
            self._dataset['pftfac'], float
        )

    def _set_evaluation_metrics(self):
        self.admission_rates = self._dataset['adm_rate']
        completion_2yr = self._dataset['overall_yr2_n']
        completion_3yr = self._dataset['overall_yr3_n']
        completion_4yr = self._dataset['overall_yr4_n']
        completion_6yr = self._dataset['overall_yr6_n']
        completion_8yr = self._dataset['overall_yr8_n']
        self.completion_rate_avg = self._data_processor._list_average([
            completion_2yr,
            completion_3yr,
            completion_4yr,
            completion_6yr,
            completion_8yr
        ])
        self.sat_scores = self._dataset['sat_avg']


class StudentData(Dataset):

    def __init__(self, path='https://raw.githubusercontent.com/alisoltanirad/'
                            'CDA/main/cda/college_scorecard/'
                            'college_scorecard.csv'):
        Dataset.__init__(self, path)
        self._set_general_info()
        self._set_race_info()
        self._set_family_info()

    def get_info(self):
        data = {
            'Name': self.college_names,
            'Ownership': self.ownership,
            'Part_Time_Share': self.part_time_share,
            'Race_White': self.race_white,
            'Race_Black': self.race_black,
            'Race_Hispanic': self.race_hispanic,
            'Race_Asian': self.race_asian,
            'Race_AIAN': self.race_aian,
            'Race_NHPI': self.race_nhpi,
            'Race_Mixed': self.race_mixed,
            'Family_Income_Dependent': self.family_income_dependent,
            'Family_Income_Independent': self.family_income_independent,
        }
        return pd.DataFrame(data)

    def _set_general_info(self):
        self.part_time_share = self._mis_value_filler.mean(
            self._dataset['pptug_ef'], float
        )

    def _set_race_info(self):
        self.race_white = self._mis_value_filler.mean(
            self._dataset['ugds_white'], float
        )
        self.race_black = self._mis_value_filler.mean(
            self._dataset['ugds_black'], float
        )
        self.race_hispanic = self._mis_value_filler.mean(
            self._dataset['ugds_hisp'], float
        )
        self.race_asian = self._mis_value_filler.mean(
            self._dataset['ugds_asian'], float
        )
        self.race_aian = self._mis_value_filler.mean(
            self._dataset['ugds_aian'], float
        )
        self.race_nhpi = self._mis_value_filler.mean(
            self._dataset['ugds_nhpi'], float
        )
        self.race_mixed = self._mis_value_filler.mean(
            self._dataset['ugds_2mor'], float
        )

    def _set_family_info(self):
        self.family_income_dependent = self._mis_value_filler.mean(
            self._dataset['dep_inc_n'], int
        )
        self.family_income_independent = self._mis_value_filler.mean(
            self._dataset['ind_inc_n'], int
        )


class FinancialData(Dataset):

    def __init__(self, path='https://raw.githubusercontent.com/alisoltanirad/'
                            'CDA/main/cda/college_scorecard/'
                            'college_scorecard.csv'):
        Dataset.__init__(self, path)
        self._set_cost_info()
        self._set_aid_info()
        self._set_family_info()

    def get_cost_info(self):
        data = {
            'Name': self.college_names,
            'Ownership': self.ownership,
            'Net_Price': self.net_price,
            'Attendance_Cost': self.attendance_cost,
            'Tuition_In_State': self.tuition_in_state,
            'Tuition_Out_State': self.tuition_out_state,
        }
        return pd.DataFrame(data)

    def get_aid_info(self):
        data = {
            'Name': self.college_names,
            'Ownership': self.ownership,
            'Title_IV': self.title_iv,
            'Federal_Loan_Rate': self.federal_loan_rate,
            'Debt_Overall': self.debt_overall,
            'Debt_Completers': self.debt_completers,
            'Debt_NonCompleters': self.debt_noncompleters,
            'Debt_Dependent': self.debt_dependent,
            'Debt_Independent': self.debt_independent,
            'Family_Income_Dependent': self.family_income_dependent,
            'Family_Income_Independent': self.family_income_independent,
        }
        return pd.DataFrame(data)

    def _set_cost_info(self):
        self.net_price = self._mis_value_filler.mean(
            self._data_processor._list_merge(
                self._dataset['npt4_pub'],
                self._dataset['npt4_priv'],
                self.ownership
            ), int
        )
        self.attendance_cost = self._mis_value_filler.mean(
            self._dataset['costt4_a'], int
        )
        self.tuition_in_state = self._mis_value_filler.mean(
            self._dataset['tuitionfee_in'], int
        )
        self.tuition_out_state = self._mis_value_filler.mean(
            self._dataset['tuitionfee_out'], int
        )

    def _set_aid_info(self):
        self.title_iv = self._mis_value_filler.mean(
            self._data_processor._list_merge(
                self._dataset['num4_pub'],
                self._dataset['num4_priv'],
                self.ownership
            ), int
        )
        self.federal_loan_rate = self._mis_value_filler.mean(
            self._dataset['pctfloan'], float
        )
        self.debt_overall = self._mis_value_filler.mean(
            self._dataset['debt_mdn_supp'], int
        )
        self.debt_completers = self._mis_value_filler.mean(
            self._dataset['grad_debt_mdn'], float
        )
        self.debt_noncompleters = self._mis_value_filler.mean(
            self._dataset['wdraw_debt_mdn'], float
        )
        self.debt_dependent = self._mis_value_filler.mean(
            self._dataset['dep_debt_mdn'], int
        )
        self.debt_independent = self._mis_value_filler.mean(
            self._dataset['ind_debt_mdn'], int
        )

    def _set_family_info(self):
        self.family_income_dependent = self._mis_value_filler.mean(
            self._dataset['dep_inc_n'], int
        )
        self.family_income_independent = self._mis_value_filler.mean(
            self._dataset['ind_inc_n'], int
        )


class MetaData:

    def __init__(self, path='https://raw.githubusercontent.com/alisoltanirad/'
                            'CDA/main/cda/college_scorecard/'
                            'college_scorecard_data_dictionary.csv'):
        ssl._create_default_https_context = ssl._create_unverified_context
        self._dataset = pd.read_csv(path)

    def get_attribute_names(self):
        return self._dataset['developer_friendly_name']
