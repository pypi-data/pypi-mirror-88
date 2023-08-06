from matplotlib import pyplot as plt

from .college_scorecard import FinancialData


class CostInfo:

    def __init__(self, path):
        self._data = FinancialData(path).get_cost_info()

    def get(self):
        return self._data

    def export(self, path='cost_data.csv'):
        self._data.to_csv(path, index=False)

    def plot_net_price_avg(self):
        categories, numbers = self._get_net_price_avg()

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.bar(categories, numbers)
        plt.title('Net Price\n (Avg. Attendance Cost Minus Avg. Financial Aid)')
        plt.ylabel('$')
        plt.show()

    def _get_net_price_avg(self):
        net_price_avg_public = self._data.loc[
            self._data['Ownership'] == 'public'
        ]['Net_Price'].astype(float).mean()
        net_price_avg_private = self._data.loc[
            self._data['Ownership'] == 'private'
        ]['Net_Price'].astype(float).mean()

        categories = ['Public-Schools', 'Private-Schools']
        numbers = [net_price_avg_public, net_price_avg_private]

        return categories, numbers
