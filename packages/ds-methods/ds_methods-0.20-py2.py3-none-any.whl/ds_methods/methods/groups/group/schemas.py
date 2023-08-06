from schema import Schema, And, Or, Optional


# grouping parameters
# keys - by which columns
# time - hours
options_schema = Schema(
    And({
        Optional('keys'): And([str], len),
        Optional('time'): And(Or(int, float), lambda x: 0 < x),
    }, lambda x: 'keys' in x or 'time' in x),
    ignore_extra_keys=True,
)
