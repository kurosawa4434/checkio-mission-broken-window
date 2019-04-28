"""
CheckiOReferee is a base referee for checking you code.
    arguments:
        tests -- the dict contains tests in the specific structure.
            You can find an example in tests.py.
        cover_code -- is a wrapper for the user function and additional operations before give data
            in the user function. You can use some predefined codes from checkio.referee.cover_codes
        checker -- is replacement for the default checking of an user function result. If given, then
            instead simple "==" will be using the checker function which return tuple with result
            (false or true) and some additional info (some message).
            You can use some predefined codes from checkio.referee.checkers
        add_allowed_modules -- additional module which will be allowed for your task.
        add_close_builtins -- some closed builtin words, as example, if you want, you can close "eval"
        remove_allowed_modules -- close standard library modules, as example "math"

checkio.referee.checkers
    checkers.float_comparison -- Checking function fabric for check result with float numbers.
        Syntax: checkers.float_comparison(digits) -- where "digits" is a quantity of significant
            digits after coma.

checkio.referee.cover_codes
    cover_codes.unwrap_args -- Your "input" from test can be given as a list. if you want unwrap this
        before user function calling, then using this function. For example: if your test's input
        is [2, 2] and you use this cover_code, then user function will be called as checkio(2, 2)
    cover_codes.unwrap_kwargs -- the same as unwrap_kwargs, but unwrap dict.

"""

from checkio.signals import ON_CONNECT
from checkio import api
from checkio.referees.io import CheckiOReferee
from checkio.referees import cover_codes
from tests import TESTS


def checker(pieces, answer):

    if not (isinstance(answer, (tuple, list))
            and len(answer) == 2
            and isinstance(answer[0], list)
            and isinstance(answer[1], list)):
        return False, (answer, 'Wrong type')

    if set(answer[0]+answer[1]) != set(range(len(pieces))):
        return False, (answer, 'Wrong value')

    tops = [list(reversed(pieces[t])) for t in answer[0]]
    bottoms = [pieces[b] for b in answer[1]]
    height = set()

    top = tops.pop(0)
    bottom = bottoms.pop(0)
    while True:
        height |= set(map(sum, zip(top, bottom)))
        if len(top) < len(bottom) and tops:
            bottom = bottom[len(top)-1:]
            top = tops.pop(0)
        elif len(top) > len(bottom) and bottoms:
            top = top[len(bottom)-1:]
            bottom = bottoms.pop(0)
        elif len(top) == len(bottom):
            if tops and bottoms:
                top = tops.pop(0)
                bottom = bottoms.pop(0)
            elif not tops and not bottoms:
                break
            else:
                return False, (answer, 'Fail')
        else:
            return False, (answer, 'Fail')

    if len(height) == 1:
        return True, (answer, 'Success')
    else:
        return False, (answer, 'Fail')


api.add_listener(
    ON_CONNECT,
    CheckiOReferee(
        tests=TESTS,
        function_name={
            "python": "broken_window",
            "js": "brokenWindow"
        },
        checker=checker,
        cover_code={
            # 'python-3': cover_codes.unwrap_args,
            # 'js-node': cover_codes.js_unwrap_args
        },
    ).on_ready)
