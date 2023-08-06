from pandas import DataFrame

from ds_methods.common.df import DataFrameUtils
from ds_methods.common.types import MethodOutput

from ds_methods.methods.base import BaseMethod

from .schemas import options_schema


class Diff(BaseMethod):
    options_schema = options_schema

    def make_(self, input_data: DataFrame) -> MethodOutput:
        numeric_part, other_part = DataFrameUtils.decompose(input_data)

        return MethodOutput(
            data=DataFrameUtils.concatenate([
                other_part,
                numeric_part.diff(self.options['periods']),
            ]),
            error=None,
        )
