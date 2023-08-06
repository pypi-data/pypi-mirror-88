from matplotlib import pyplot as plt
import seaborn as sns

from ds_methods.common.utils import categories_to_colors
from ds_methods.methods.pipeline import Pipeline
from ds_methods.methods.filters import *
from ds_methods.methods.preprocessing import *
from ds_methods.methods.groups import *
from ds_methods.methods.analysis import *

from ds_methods.templates.init_data import load_raw_data

data = load_raw_data()
data = data[data['condition'] == 'infected']

pca_group_time = 24

data = Pipeline([
    Group({
        'keys': ['target'],
    }),
    Normalisation({
        'type': 'z_score',
    }),
    # Group({
    #     'keys': ['target'],
    # }),
    # SeasonalDecomposition({
    #     'period': 60 * 24 // 8,
    # }),
    Group({
        'keys': ['target'],
        'time': pca_group_time,
    }),
    Basic({
        'method': 'mean',
    }),
]).run(data)['data']


data = PCA({
    'components': 2,
}).make(data.dropna())['data']

_, ax = plt.subplots(figsize=(12, 12))

sns.scatterplot(data=data, hue='group', x=data.columns[0], y=data.columns[1], s=100)
plt.legend(loc=2)
plt.title(f'PCA for all (healthy) mice, by {pca_group_time} hours, colored by group\n'
          'Z-Score norm.')

plt.savefig(f'plots/pca_for_all_healthy_by_group.png')
data.to_csv('pca_for_all_healthy_by_group.csv', index=False)
#
# data = load_raw_data(is_polynomials=True)
#
# for name, group in data.groupby('group'):
#     group = Pipeline([
#         Group({
#             'keys': ['target'],
#         }),
#         Normalisation({
#             'type': 'z_score',
#         }),
#         # Group({
#         #     'keys': ['target'],
#         # }),
#         # SeasonalDecomposition({
#         #     'period': 60 * 24 // 8,
#         # }),
#         Group({
#             'keys': ['target'],
#             'time': pca_group_time,
#         }),
#         Basic({
#             'method': 'mean',
#         }),
#         PCA({
#             'components': 2,
#         }),
#     ]).run(group)['data']
#
#     _, ax = plt.subplots(figsize=(12, 12))
#
#     sns.scatterplot(data=group, hue='group', x=group.columns[0], y=group.columns[1], s=100)
#
#     plt.legend(loc=2)
#     plt.title(f'PCA for {name} mice, by {pca_group_time} hours, colored by group\n'
#               'Z-Score norm.')
#
#     plt.savefig(f'plots/pca_for_{name}_group.png')
#     data.to_csv(f'pca_for_{name}_group.csv', index=False)
