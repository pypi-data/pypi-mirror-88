from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.cm as cm

from ds_methods.common.df import DataFrameUtils
from ds_methods.methods.groups import *
from ds_methods.methods.preprocessing import Resampling

pd.set_option('mode.chained_assignment', None)


POINTS_RANGE = (1000, 5000)
N_GROUPS = 3
N_INSTANCES = 10
N_FEATURES = 10
COLORS = cm.rainbow(np.linspace(0, 1, N_INSTANCES))


def load_raw_data(is_full=False, is_polynomials=False, n_resample_minutes: int = 4, is_only_full: bool = False):
    period = 24 * 60 // n_resample_minutes

    try:
        if is_polynomials:
            data = pd.read_csv(f'./mice_data_polynomials.csv')
        else:
            data = pd.read_csv(f'./{n_resample_minutes}_cleared_mice_data.csv')
        data['target'] = data['target'].astype(int).astype(str)
        data['date'] = pd.to_datetime(data['date'], utc=True).dt.tz_localize(None)
    except Exception:
        data = pd.read_csv('./mica_data.csv' if is_full else './mica_data_100.csv')

        data['date'] = pd.to_datetime(data['date'], utc=True).dt.tz_localize(None)
        data = data[data['date'] >= datetime(2020, 11, 1)]
        data['condition'] = data['is_sick'].copy()
        data['condition'][~data['is_sick']] = 'healthy'
        data['condition'][data['is_sick']] = 'infected'

        data['group'][data['target'] <= 27] = 'Group 0'
        data['group'][data['target'] > 27] = 'Group 1'

        data['target'] = data['target'].astype(str)

        data = data.drop(['is_sick', 'row'], axis=1)

        data = Group({'keys': ['target']}) \
            .make(data)['data'] \
            .apply(lambda group: Resampling({'rule': f'{n_resample_minutes}Min'}) \
            .make(group)['data']) \
            .reset_index(drop=True)

        numeric_columns = data.select_dtypes(['number']).columns

        for mouse_name in data['target'].unique():
            mouse_data = data[data['target'] == mouse_name]

            first_date = mouse_data['date'].iloc[0]
            first_day = datetime.combine(first_date.date(), datetime.min.time())

            missed_first_minutes = (first_date.to_pydatetime() - first_day).seconds // 60
            missed_rows = missed_first_minutes // n_resample_minutes

            if missed_rows > 0:
                dates = pd.date_range(
                    first_day,
                    periods=missed_rows,
                    freq=f'{n_resample_minutes}Min',
                )

                # print('here 1', data)
                data = pd.concat([
                    data.iloc[:mouse_data.index[0]],
                    mouse_data.iloc[:missed_rows],
                    data.iloc[mouse_data.index[0]:],
                ], axis=0).reset_index(drop=True)
                data.iloc[mouse_data.index[0]: mouse_data.index[0] + missed_rows]['date'] = dates
                data.iloc[mouse_data.index[0]: mouse_data.index[0] + missed_rows][numeric_columns] = np.nan

        numeric_part, other_part = DataFrameUtils.decompose(data)
        data[numeric_part.columns] = data[numeric_part.columns].fillna(numeric_part.mean())
        data[other_part.columns] = data[other_part.columns].fillna(method='bfill')
        print(data)

        data.to_csv(f'{n_resample_minutes}_cleared_mice_data.csv', index=False)

    if is_only_full:
        day_groups = Group({'keys': ['target'], 'time': 24}).make(data)['data']
        data = data[day_groups.transform(lambda x: len(x) == period).astype('bool')['condition']]

    return data


def make_fake_data(
        points_range=POINTS_RANGE,
        n_groups=N_GROUPS,
        n_instances=N_INSTANCES,
        n_features=N_FEATURES,
        colors=COLORS,
):
    data = []
    for instance in range(n_instances):
        features = []
        n_points = np.random.randint(*points_range)
        dates = pd.date_range(
            datetime(2020, 10, 10, 1, 00),
            periods=n_points,
            freq='27min',
        )
        linespace = np.linspace(0, 10 * np.pi, n_points)
        for feature in range(n_features):
            func = np.sin if feature % 2 else np.cos
            noise = np.random.random(n_points)
            features.append(
                func(linespace) * noise + 0.1 * noise,
            )

        for sample in range(n_points):
            data.append({
                'instance': f'instance_{instance}',
                'group': f'group_{instance % n_groups}',
                'date': dates[sample],
                'state': 'healthy' if sample <= n_points // 2 else 'sick',
                **{
                    f'feature_{feature}': features[feature][sample]
                    for feature in range(n_features)
                },
            })

    return pd.DataFrame(data)

# INIT_DATA = make_fake_data()
