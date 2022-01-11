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
        help='Run the test file',
        action='store_true'
    ) #Comment for production

    parser.add_argument(
        '-o',
        help='Name of the output file(s)',
        default='output'
    )

    cli = parser.parse_args()

    if cli.version:
        print(f"{__app_name__} v {__version__}")
        exit()

    if cli.test:
        import optimizer.test
        exit()

    return cli
