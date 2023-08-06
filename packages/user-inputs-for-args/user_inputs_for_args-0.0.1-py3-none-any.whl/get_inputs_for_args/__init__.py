"""
contains get_param_input wrapper
"""
from functools import wraps, partial
import re


help_menu = """
While entering the values for the params, If you would like the:
    function description : --func-desc
    print this help menu : --help-menu
    parameter help       : --help"""


def get_arg_doc_anns(all_arg_names: list, doc_str: str) -> dict:
    """
    It splits the docstring for each time the param indicator came up. It loops through the values, and for each value
    if there was no return indicator in that string, it would just save the arg name and and it's annotation, but if it
    did have the return indicator in the string, it would get the index of where it is, and split the string using it's
    index into two parts, the param_ann and the retrn_ann. These are then both split by ': '. It then loops through both
    of them and for each ann it saves the arg and ann in the format {arg: ann}. After that, it checks if there is an
    annotation for all the args, and if there isn't, it adds missing args with a description saying 'no arg description'

    :param all_arg_names: all of the names of the funcs args
    :param doc_str: the functions docstring
    :return: a dict of each arg and its doc_annotation
    """
    arg_descs = {}
    split_doc_str = doc_str.split('\n    :param ')[1:]
    for extract in split_doc_str:
        arg_name, arg_desc = re.split(r'\n\s{4}:return: |\n\s{4}$', extract)[0].split(': ')
        arg_descs.update({arg_name: arg_desc.replace('\n    ', '\n')})

    if not set(all_arg_names) == set(arg_descs.keys()):
        missing_args = set(all_arg_names) - set(arg_descs.keys())
        for missing_arg in missing_args:
            arg_descs.update({missing_arg: 'No description'})

    return arg_descs


def get_args_anns(all_arg_names: list, kwarg_names: iter, current_anns: dict) -> list:
    """
    gets all the args of a function, an uncompleted dict of annotations with the format: {arg: type}, and a list of the
    already annotated args. Then, it makes a list called annotations that will be the output. It loops through each arg.
    If it is already annotated, it is added to annoations in a dict with the format {'name': arg, 'type': type}.
    If it is not already annotated, it is added to annotations in a dict with the format {'name': arg, 'type': str}.
    When it's finished looping, it returns the annotations list.

    :param current_anns: the current annotations of this function's args
    :param kwarg_names: a tuple of all the func's kwarg names
    :param all_arg_names: all the the funcs args
    :return: a list of dict objects that contain the args and their annotations
    """
    if not all_arg_names:
        return []
    args_types = []
    posarg_names = list(filter(lambda a: a not in kwarg_names, all_arg_names))
    for arg_name in posarg_names:
        arg_type = current_anns[arg_name] if arg_name in current_anns.keys() else str
        args_types.append({'name': arg_name, 'type': arg_type})

    return args_types


def get_default_args(all_arg_names: list, kwarg_values: tuple or None) -> dict:
    """
    gets all the default values and gets the default args by taking the last {num_of_default_values} out of args as all
    default values must be at the last of the args list. Then, it loops through the default args and values and for each
    arg and value they are added to a dict with the format {arg: value}

    :param kwarg_values:
    :param all_arg_names: all the
    :return: a dict containing all args with their default values
    """
    if not kwarg_values or not all_arg_names:
        return {}
    kwarg_names = all_arg_names[-len(kwarg_values):]
    return dict(zip(kwarg_names, kwarg_values))


def get_inputs_for_args(func=None, test_inputs: iter = None) -> callable:
    """
    a decorator that wraps the given function in a wrapper that gets inputs for args that haven't been entered
    programmatically from the user

    :param func: the function that you want to be wrapped.
    :param test_inputs: automatic inputs for testing
    :return: a wrapper that gets inputs for args that haven't been entered programmatically from the user
    """
    if func is None:
        return partial(get_inputs_for_args, test_input_gen=test_inputs)
    if func.__code__.co_argcount == 0:
        return func
    if test_inputs is not None:
        test_input_gen = (test_input for test_input in test_inputs)

    all_arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]

    all_kwargs = get_default_args(all_arg_names, func.__defaults__)
    arg_desc = get_arg_doc_anns(all_arg_names, func.__doc__)
    posargs_types = get_args_anns(all_arg_names, all_kwargs.keys(), func.__annotations__)
    help_cmd_interp = {
        '--func-desc': func.__doc__,
        '--help-menu': help_menu,
        '--help': None
    }

    @wraps(func)
    def wrapper_get_inputs_from_args(*args, **kwargs) -> any:
        """
        Adds all args with defaults to kwargs. It then saves all the args that args that have not got a default vaue or
        have not been passed in yet to args_for_user. It loops through each arg, removes _'s and tries to get an input
        from the user using the prompt: 'name (type): '. If the user actually types in a command, then it does that cmd
        and repeats the question. If the user enters the wrong type of input, then it catches the error and asks them
        to try again. Once it has got a valid input, it adds it to the kwargs dict and goes onto the next one. It
        repeats this until it has finished all the args, and then passes them into the function, and returns the result

        :param args: all positional arguments passed in
        :param kwargs: all key word arguments passed in
        :return: the result when you pass in all the args to the given func.
        """
        all_kwargs.update(kwargs)
        args_for_usr = []
        for arg in posargs_types[len(args):]:
            if arg['name'] not in all_kwargs.keys():
                args_for_usr.append((arg['name'].replace('_', ' '), arg['type']))

        print(help_menu, end='\n\n')
        print('=' * 6, func.__name__.replace('_challenge', ''), '=' * 33)

        for arg_name, arg_type in args_for_usr:
            help_cmd_interp['--help'] = ':param ' + arg_name + ': ' + arg_desc[arg_name]
            usr_input_prompt = arg_name + ' (' + arg_type.__name__ + '): '

            got_valid_input = False
            while got_valid_input is False:
                usr_input = input(usr_input_prompt) if not test_input_gen else next(test_input_gen)
                if usr_input in help_cmd_interp.keys():
                    print(help_cmd_interp[usr_input])
                    continue

                try:
                    all_kwargs.update({arg_name: arg_type(usr_input)})
                    got_valid_input = True
                except ValueError:
                    print('you typed in the wrong value type, please try again')

        print('=' * 6, 'output', '=' * 33)
        result = func(*args, **all_kwargs)
        return result

    return wrapper_get_inputs_from_args
