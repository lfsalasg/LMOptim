import argparse
import os
from optimizer import __app_name__,__version__

def parse_cli ():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input',
        help='Archivo input para la optimización',
        nargs='?',
        default='in.input'
    )

    parser.add_argument(
        '-v','--version',
        help='Version of the optimizer',
        action='store_true',
    )
    
    parser.add_argument(
        '--test',
        help='Version of the optimizer',
        action='store_true',
    )

    cli = parser.parse_args()

    if cli.version:
        print(f"{__app_name__} v {__version__}")
        exit()

    return cli