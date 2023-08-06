from libLemon.ASM.Delegate import ParamDelegate
from libLemon.Error import TypeLookupError, ExpressionValidationError


_type_str_mapper = {
    'int': int,
    'float': float,
    'bool': bool
}


def str2typ(string: str) -> type:
    for k, v in _type_str_mapper.items():
        if k == string:
            return v
    raise TypeLookupError('no appropriate type found for string `%s`' % string)


def typ2str(typee: type) -> str:
    for k, v in _type_str_mapper.items():
        if v == typee:
            return k
    raise TypeLookupError(
        'no appropriate string found for type `%s`' % str(typee))


def parse_cmd_args(args: str, maxsplit: int = -1) -> list[str]:
    return [v.strip() for v in args.split(',', maxsplit=maxsplit) if v.strip()]


def judge_condition(data_source: ParamDelegate, cond: str) -> bool:
    for param_name in data_source.get_all_params_name():
        cond = cond.replace('$%s$' % param_name,
                            '(%s)' % str(data_source.get_parameter_value(param_name)))

    if '$' in cond:
        raise ExpressionValidationError(
            'unbound variables in condition expression `%s`' % cond)

    try:
        return bool(eval(cond))
    except SyntaxError:
        raise ExpressionValidationError(
            'failed to evaluate expression `%s`' % cond)
