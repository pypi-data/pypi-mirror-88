from .college_scorecard import FinancialData


class FinancialAidInfo:

    def __init__(self, path):
        self._data = FinancialData(path).get_aid_info()

    def get(self):
        return self._data

    def export(self, path='aid_data.csv'):
        self._data.to_csv(path, index=False)

    def get_avg_debt(self):
        data = {
            'Overall': float('{:.2f}'.format(
                self._data['Debt_Overall'][
                    self._data['Debt_Overall'].values != 'PrivacySuppressed'
                ].astype(float).mean()
            )),
            'Completers': float('{:.2f}'.format(
                self._data['Debt_Completers'][
                    self._data['Debt_Completers'].values != 'PrivacySuppressed'
                ].astype(float).mean()
            )),
            'NonCompleters': float('{:.2f}'.format(
                self._data['Debt_NonCompleters'][
                    self._data['Debt_NonCompleters'].values != 'PrivacySuppressed'
                ].astype(float).mean()
            )),
            'Dependent': float('{:.2f}'.format(
                self._data['Debt_Dependent'][
                    self._data['Debt_Dependent'].values != 'PrivacySuppressed'
                ].astype(float).mean()
            )),
            'Independent': float('{:.2f}'.format(
                self._data['Debt_Independent'][
                    self._data['Debt_Independent'].values != 'PrivacySuppressed'
                ].astype(float).mean()
            )),
        }

        return data
