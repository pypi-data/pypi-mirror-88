from nextnanopy.utils.formatting import str_to_path, _path, pattern_in_file, is_variable, parse_variable, \
    generate_command, pattern_in_text
from collections import OrderedDict

fmt = {
    'var_char': 'NOT DEFINED',
    'com_char': '<!--',
    'input_pattern': '<Simulation',
}

config_validator = {
    'exe': str_to_path,
    'license': str_to_path,
    'database': str_to_path,
    'outputdirectory': str_to_path,
    'threads': int,
}

config_default = {
    'exe': '',
    'license': '',
    'database': '',
    'outputdirectory': '',
    'threads': 0,
}


def command_negf(
        inputfile,
        exe,
        license,
        database,
        outputdirectory,
        threads=0,
        **kwargs,
):
    kwargs = OrderedDict(
        exe=[_path(exe), ''],
        inputfile=[_path(inputfile), ''],
        outputdirectory=[_path(outputdirectory), ''],
        database=[_path(database), ''],
        license=[_path(license), ''],
        threads=['-threads', threads],
    )
    return generate_command(kwargs.values())


def is_negf_variable(text):
    return is_variable(text, var_char=fmt['var_char'])


def parse_negf_variable(text):
    return parse_variable(text, var_char=fmt['var_char'], com_char=fmt['com_char'])


def is_negf_input_file(fullpath):
    return pattern_in_file(fullpath, fmt['input_pattern'])


def is_negf_input_text(text):
    return pattern_in_text(text, fmt['input_pattern'])
