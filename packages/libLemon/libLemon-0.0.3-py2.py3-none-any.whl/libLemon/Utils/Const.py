"""
version control
"""
MAJOR_VERSION = 0
MINOR_VERSION = 0
PATCH_VERSION = 3

VERSION = '.'.join([str(i)
                    for i in [MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION]])

"""
magic strings
"""
ERROR_TYPE = '<< error type >>'
UNKNOWN_TYPE = '<< unknown type >>'

ASM_NAME_PREFIX = '__asm__'
MODULE_NAME_PREFIX = '__mod__'

FROM_TO_CONNECTOR = ' => '

"""
status codes
"""
STATUS_OK = '^_^ ok'
STATUS_ERR = 'x_x error'
STATUS_NO_PARAM = '?_? no param'
STATUS_BAD_TYPE = '!_! bad type'