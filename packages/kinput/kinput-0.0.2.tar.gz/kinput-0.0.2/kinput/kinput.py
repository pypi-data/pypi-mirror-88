from typing import Optional, Tuple
import builtins

def input(
    message: Optional[str] = None,
    default: Optional[any] = None,
    type = str
) -> Tuple[Optional[any], Optional[Exception]]:
    message = message or ''

    if default:
        message += '\nDefault: {}'.format(default)
    
    res = builtins.input('\n\n{}\n\n>>> '.format(message))

    if not res:
        res = default

    try:
        return type(res), None
    except Exception as e:
        return None, e