from nextnanopy.utils.formatting import str_to_path, _path, pattern_in_file, is_variable, parse_variable, \
    generate_command, pattern_in_text
from collections import OrderedDict

fmt = {
    'var_char': 'NOT DEFINED',
    'com_char': '<!--',
    'input_pattern': '<nextnano.MSB',
}

config_validator = {
    'exe': str_to_path,
    'license': str_to_path,
    'database': str_to_path,
    'outputdirectory': str_to_path,
    'debug': int,
}

config_default = {
    'exe': '',
    'license': '',
    'database': '',
    'outputdirectory': '',
    'debug': 0,
}


def command_msb(
        inputfile,
        exe,
        license,
        database,
        outputdirectory,
        debug=0,
        **kwargs,
):
    kwargs = OrderedDict(
        exe=[_path(exe), ''],
        inputfile=['-inputfile', _path(inputfile)],
        license=['-license', _path(license)],
        database=['-database', _path(database)],
        outputdirectory=['-outputdirectory', _path(outputdirectory)],
    )
    if debug == 1:
        kwargs['debug'] = ['-debug', debug]
    return generate_command(kwargs.values())


def is_msb_variable(text):
    return is_variable(text, var_char=fmt['var_char'])


def parse_msb_variable(text):
    return parse_variable(text, var_char=fmt['var_char'], com_char=fmt['com_char'])


def is_msb_input_file(fullpath):
    return pattern_in_file(fullpath, fmt['input_pattern'])


def is_msb_input_text(text):
    return pattern_in_text(text, fmt['input_pattern'])
