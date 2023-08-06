from pandas import DataFrame

from ds_methods.common.df import DataFrameUtils
from ds_methods.common.validators import check_keys, check_datetime
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import options_schema


class MovingAverage(BaseMethod):
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        numeric_part, other_part = DataFrameUtils.decompose(input_data)
        if self.options.get('window'):
            numeric_part = numeric_part.rolling(window=self.options['window'], center=True).mean()
        else:
            numeric_part.index = other_part['date']
            numeric_part = numeric_part\
                .rolling(window=self.options['time'])\
                .mean()\
                .reset_index(drop=True)

        return MethodOutput(
            data=DataFrameUtils.concatenate([other_part, numeric_part]),
            error=None,
        )

    def validate_input_(self, input_data: DataFrame) -> bool:
        if self.options.get('window') and self.options['window'] <= len(input_data.index):
            return True
        if self.options.get('time') and check_keys(input_data, ['date']) and check_datetime(input_data['date']):
            return True

        return False
