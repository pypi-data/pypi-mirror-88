"""
tests get_inputs_for_args func

get_inputs_for_args features:
  ✔ you can input help cmds and it will print help statement then ask again for input for arg
  ✔ it will convert the inputted value to the desired type
  ✔ it won't let you input values for args with default args
  ✔ It will ask for input again if input is invalid
"""
import pytest
from get_inputs_for_args import get_inputs_for_args


def help_cmds(arg1, arg2, arg3, arg4, arg5, arg6) -> tuple:
    """one"""
    return arg1, arg2, arg3, arg4, arg5, arg6


def avoid_kwargs(arg1, arg2, arg3, arg4=1, arg5=1, arg6=1) -> tuple:
    """one"""
    return arg1, arg2, arg3, arg4, arg5, arg6


def handle_inputs(arg1: int, arg2: int, arg3: int, arg4: int, arg5: int, arg6: int) -> tuple:
    """convert arg type"""
    return arg1, arg2, arg3, arg4, arg5, arg6


def convert_arg_type_int(arg1: int, arg2: int, arg3: int, arg4: int, arg5: int, arg6: int) -> tuple:
    """convert arg type"""
    return arg1, arg2, arg3, arg4, arg5, arg6


def convert_arg_type_flt(arg1: float, arg2: float, arg3: float, arg4: float, arg5: float, arg6: float) -> tuple:
    """convert arg type"""
    return arg1, arg2, arg3, arg4, arg5, arg6


def convert_arg_type_bool(arg1: bool, arg2: bool, arg3: bool, arg4: bool, arg5: bool, arg6: bool) -> tuple:
    """convert arg type"""
    return arg1, arg2, arg3, arg4, arg5, arg6


@pytest.mark.parametrize('test_inputs', [
    ('1', '2', '3', '4', '--help', '5', '6'),
    ('1', '2', '3', '4', '--help', '--help-menu', '5', '6'),
    ('1', '2', '--func-desc', '3', '4', '5', '6'),
    ('1', '--func-desc', '--help-menu', '2', '3', '4', '5', '6'),
    ('1', '2', '3', '4', '--help', '5', '6'),
])
def test_get_inputs_for_args_help_cmds(test_inputs) -> None:
    """
    tests get_inputs_for_args()
    """
    get_inputs_for_args(func=help_cmds, test_inputs=test_inputs)()


@pytest.mark.parametrize('convert_arg_type_func, test_inputs, expected', [
    (convert_arg_type_int, ('1', '2', '3', '4', '5', '6'), (1, 2, 3, 4, 5, 6)),
    (convert_arg_type_int, ('3', '7', '9', '18', '30', '4'), (3, 7, 9, 18, 30, 4)),
    (convert_arg_type_int, ('15', '322', '423', '324', '51', '685'), (15, 322, 423, 324, 51, 685)),
    (convert_arg_type_flt, ('1.4', '2.4', '3.4', '4.4', '5.4', '6.4'), (1.4, 2.4, 3.4, 4.4, 5.4, 6.4)),
    (convert_arg_type_flt, ('3.4', '7.4', '9.4', '18.4', '30.4', '4.4'), (3.4, 7.4, 9.4, 18.4, 30.4, 4.4)),
    (convert_arg_type_flt, ('15.4', '32.4', '43.4', '34.4', '51.4', '65.4'), (15.4, 32.4, 43.4, 34.4, 51.4, 65.4)),
    (convert_arg_type_bool, ('True', '', '', 'foo', '', 'boo'), (True, False, False, True, False, True)),
])
def test_get_inputs_for_args_convert_arg_type(convert_arg_type_func, test_inputs, expected) -> None:
    """
    tests get_inputs_for_args()
    """
    actual_values = get_inputs_for_args(func=convert_arg_type_func, test_inputs=test_inputs)()
    assert actual_values == expected


@pytest.mark.parametrize('should_fail, test_inputs', [
    (False, ('1', 'FILL', 'FILL', '2', '3', 'FILL', '4', '5', '6')),
    (False, ('1', '2', '3', '4', '5', '6')),
    (False, ('1', '2', '3', '4', 'FILL', '5', '6')),
    (True, ('FILL', '2', '3', '4', '5', '6')),
    (True, ('1', 'FILL', '3', '4', '5', '6')),
    (True, ('1', 'FILL', '2', '3', 'FILL', '5', '6')),
])
def test_get_inputs_for_args_handle_inputs(should_fail, test_inputs) -> None:
    """
    tests get_inputs_for_args()
    """
    returned_args = ()
    try:
        returned_args = get_inputs_for_args(func=convert_arg_type_int, test_inputs=test_inputs)()
    except StopIteration:
        assert should_fail is True

    if should_fail is False:
        assert returned_args == (1, 2, 3, 4, 5, 6)


@pytest.mark.parametrize('test_inputs, expected', [
    (('1', '2', '3', '4', '5', '6'), ('1', '2', '3', 1, 1, 1)),
    (('1', '2', '3', '4', '5', '6', '7'), ('1', '2', '3', 1, 1, 1)),
])
def test_get_inputs_for_args_avoid_kwargs(test_inputs, expected) -> None:
    """
    tests get_inputs_for_args()
    """
    returned_values = get_inputs_for_args(func=avoid_kwargs, test_inputs=test_inputs)()
    assert returned_values == expected
