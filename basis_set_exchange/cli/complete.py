'''
Completers & validators for argcomplete
'''

import os
import typing
from .. import api, curate, writers, readers


def _fix_datadir(data_dir: str) -> str:
    # Handle tilde and variables. These may not have
    # been substituted by the shell at this point
    if data_dir:
        data_dir = os.path.expanduser(data_dir)
        data_dir = os.path.expandvars(data_dir)
    return data_dir


def cli_case_insensitive_validator(s1: str, s2: str) -> bool:
    s1 = s1.lower()
    s2 = s2.lower()
    return s1.startswith(s2)


def cli_bsname_completer(**kwargs) -> typing.List[str]:
    # Get the data dir if it has been specified already
    data_dir = _fix_datadir(kwargs['parsed_args'].data_dir)
    return api.get_all_basis_names(data_dir)


def cli_family_completer(**kwargs) -> typing.List[str]:
    # Get the data dir if it has been specified already
    data_dir = _fix_datadir(kwargs['parsed_args'].data_dir)
    return api.get_families(data_dir)


def cli_write_fmt_completer(**kwargs) -> typing.Dict[str, typing.Dict[str, str]]:
    return writers.get_writer_formats()


def cli_read_fmt_completer(**kwargs) -> typing.Dict[str, typing.Dict[str, str]]:
    return readers.get_reader_formats()


def cli_reffmt_completer(**kwargs) -> typing.Dict[str, str]:
    return api.get_reference_formats()


def cli_role_completer(**kwargs) -> typing.Dict[str, str]:
    return api.get_roles()


def cli_readerfmt_completer(**kwargs):
    return curate.get_reader_formats()
