from schema import Schema, And, Optional


options_schema = Schema(
    {
        'period': And(int, lambda x: 1 <= x),
        Optional('is_extrapolate', default=False): bool,
    },
    ignore_extra_keys=True,
)
