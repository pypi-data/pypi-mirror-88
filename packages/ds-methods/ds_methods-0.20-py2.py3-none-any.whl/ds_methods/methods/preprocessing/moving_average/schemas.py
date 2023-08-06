from schema import Schema, And, Optional


options_schema = Schema(
    And({
        Optional('window'): And(int, lambda x: 1 <= x),
        Optional('time'): str,
    }, lambda x: 'window' in x or 'time' in x),
    ignore_extra_keys=True,
)
