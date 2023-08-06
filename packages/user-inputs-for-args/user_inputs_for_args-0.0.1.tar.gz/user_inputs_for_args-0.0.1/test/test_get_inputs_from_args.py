"""
tests get_inputs_for_args
"""
import get_inputs_for_args
import pytest


@pytest.mark.parametrize('doc_str, expected', [
    ("""word word word word word word word word word word
    word word word word word

    word word word word word word
    word
    
    :param 1: word word word word
    word word word word
    :param 2: word word word
    
    bruh
    :param 3: word word word
    
    :param 4: word
    :return: words
    """, {
        '1': 'word word word word\nword word word word',
        '2': 'word word word\n\nbruh',
        '3': 'word word word',
        '4': 'word',
        '5': 'No description'
    }), ("""word word word word word word word word word word
    word word word word word

    word word word word word word
    word
    
    :param 1: word word word word
    word word word word
    :param 2: word word word
    
    bruh
    :param 3: word word word
    
    :param 4: word
    """, {
        '1': 'word word word word\nword word word word',
        '2': 'word word word\n\nbruh',
        '3': 'word word word',
        '4': 'word',
        '5': 'No description'
    }),
])
def test_get_arg_doc_anns(doc_str, expected) -> None:
    """
    tests get_arg_doc_anns()
    """
    actual_ouput = get_inputs_for_args.get_arg_doc_anns(['1', '2', '3', '4', '5'], doc_str)
    assert actual_ouput == expected


@pytest.mark.parametrize('all_arg_names, kwarg_names, current_anns, expected', [
    (['1', '2', '3', '4', '5', '6'], ['3', '2'], {'4': int}, [
        {'name': '1', 'type': str},
        {'name': '4', 'type': int},
        {'name': '5', 'type': str},
        {'name': '6', 'type': str},
    ]),
    (['1', '2', '3', '4', '5', '6'], ['5', '1', '3'], {'2': float, '4': range}, [
        {'name': '2', 'type': float},
        {'name': '4', 'type': range},
        {'name': '6', 'type': str},
    ]),
    (['1', '2', '3', '4', '5', '6'], ['1', '3', '4', '6'], {'5': int}, [
        {'name': '2', 'type': str},
        {'name': '5', 'type': int},
    ]),
    (['1', '2', '3', '4', '5', '6'], ['1', '3', '4', '6'], {}, [
        {'name': '2', 'type': str},
        {'name': '5', 'type': str},
    ]),
    ([], [], {}, []),
])
def test_get_args_anns(all_arg_names, kwarg_names, current_anns, expected) -> None:
    """
    tests get_args_anns()
    """
    actual_ouput = get_inputs_for_args.get_args_anns(all_arg_names, kwarg_names, current_anns)
    assert actual_ouput == expected


@pytest.mark.parametrize('kwarg_values, expected', [
    ((1, 2), {
        'arg5': 1,
        'arg6': 2,
    }),
    ((1, 2, 3), {
        'arg4': 1,
        'arg5': 2,
        'arg6': 3,
    }),
    ((1, 2, 3, 4, 5), {
        'arg2': 1,
        'arg3': 2,
        'arg4': 3,
        'arg5': 4,
        'arg6': 5,
    }),
    ((1, 2, 3, 4), {
        'arg3': 1,
        'arg4': 2,
        'arg5': 3,
        'arg6': 4,
    }),
    (None, {}),
])
def test_get_default_args(kwarg_values, expected) -> None:
    """
    tests get_default_args()
    """
    all_arg_names = ['arg1', 'arg2', 'arg3', 'arg4', 'arg5', 'arg6']
    actual_output = get_inputs_for_args.get_default_args(all_arg_names, kwarg_values)
    assert actual_output == expected
