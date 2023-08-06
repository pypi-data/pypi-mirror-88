__author__ = 'Milo Utsch and Cecília Assis'
__version__ = '0.1.0'

import os
import typing as tp

import pandas as pd

DF = pd.DataFrame
StrOrDataframe = tp.Union[str, DF]


def read_dataframe(dataframe: StrOrDataframe, sep: str = '|', encoding: str = 'utf-8') -> DF:
    """Provides a dataframe.

    If `dataframe` is a string it will read the file, otherwise it returns the passed object.

    Parameters
    ----------
    dataframe : str | pandas.DataFrame
        Dataframe object, can be a file to be read.
    sep : str, optional
        CSV separator (default is "|").
    encoding : str, optional
        File encoding (default is utf-8).

    Returns
    -------
    dataframe : pandas.DataFrame
        Read dataframe.

    Raises
    ------
    TypeError
        If `dataframe` is not the expected type.
    """
    if isinstance(dataframe, str):
        return read_from_file(file_name=dataframe, sep=sep, encoding=encoding)
    elif isinstance(dataframe, DF):
        return dataframe
    else:
        raise TypeError('Dataframe must be `str` or `pandas.DataFrame`.')


def read_from_file(file_name: str, sep: str = '|', encoding: str = 'utf-8') -> DF:
    """Reads dataframe from file.

    Parameters
    ----------
    file_name : str
        Name of the file to be read.
    sep : str, optional
        CSV separator (default is "|").
    encoding : str, optional
        File encoding (default is utf-8).

    Returns
    -------
    dataframe : pandas.DataFrame
        Read dataframe.

    Raises
    ------
    FileNotFoundError
        If `file_name` not found.
    """
    if os.path.isfile(file_name):
        return pd.read_csv(filepath_or_buffer=file_name, sep=sep, encoding=encoding)
    else:
        raise FileNotFoundError(f"File at '{file_name}' not found.")
