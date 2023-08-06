import pandas as pd
from matplotlib import pyplot as plt

from ds_methods.common.df import DataFrameUtils
from ds_methods.methods.pipeline import Pipeline
from ds_methods.methods.filters import *
from ds_methods.methods.preprocessing import *
from ds_methods.methods.groups import *
from ds_methods.templates.init_data import load_raw_data
from ds_methods.templates.analysis.polyfit.consts import *
from ds_methods.templates.analysis.polyfit.utils import *


data = load_raw_data(is_only_full=True, n_resample_minutes=RESAMPLE_MINUTES)

data = Pipeline([
    Group({'keys': ['target']}),
    FilterOutliers({'threshold': 3, 'how': 'any'}),
    Group({'keys': ['target']}),
    MovingAverage({'time': '2h'}),
]).run(data)['data']


def make_polynomial(group):
    numeric, _ = DataFrameUtils.decompose(group)

    for column in numeric.columns:
        group[column] = get_polynomial_info(group[column], INTERPOLATION_SPARCING)['data']

    return group

def make_polynomial_dataframe():
    print(data)
    result = data.groupby('target').apply(make_polynomial)

    print(result)

    result.to_csv('mice_data_polynomials.csv', index=False)

    _, ax = plt.subplots()
    result.groupby('target').plot(y='area', x='date', ax=ax)
    plt.savefig('test.png')

    return result


if __name__ == '__main__':
    make_polynomial_dataframe()
