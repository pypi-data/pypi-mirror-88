"""
version control
"""
MAJOR_VERSION = 0
MINOR_VERSION = 0
PATCH_VERSION = 2

VERSION = '.'.join([str(i)
                    for i in [MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION]])

"""
magic strings
"""
ERROR_TYPE = '<< error type >>'
UNKNOWN_TYPE = '<< unknown type >>'

ASM_NAME_PREFIX = '__asm__'
MODULE_NAME_PREFIX = '__mod__'

SCHEDULE_REQUEST_MESSAGE = 'ASM ++> Module (^_^)'
SCHEDULE_RESPONSE_MESSAGE = 'ASM <++ Module (^_^)'

LEFT_ARROW = ' <- '
RIGHT_ARROW = ' -> '

FROM_TO_CONNECTOR = ' => '

YIELD_MESSAGE = 'ASM <~~ Module (x_x)'

GET_PARAM_HEADER = 'ASM -@-> Module'
PUT_PARAM_HEADER = 'ASM <-&- Module'
