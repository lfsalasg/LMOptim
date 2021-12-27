from optimizer import cli, __app_name__
from optimizer import main
arg = cli.parse_cli()

main.main(arg.input)