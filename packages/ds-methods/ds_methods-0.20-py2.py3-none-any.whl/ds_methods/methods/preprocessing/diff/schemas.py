from schema import Schema, And, Optional


options_schema = Schema(
    {Optional('periods', default=1): And(int, lambda x: x >= 1)},
    ignore_extra_keys=True,
)
