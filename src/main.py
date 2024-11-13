import logging
import platform

from src.user_interfaces.command_line_interface import CommandLineInterface
from src.manager import Manager
from src.project_types import InputArgs

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info(platform.python_version())

    cli = CommandLineInterface()
    try:
        input_args = cli.get_init_data()
        manager = Manager(input_args)
        manager.create_report()
    except Exception as e:
        print(e)
    

if __name__ == "__main__":
    main()
