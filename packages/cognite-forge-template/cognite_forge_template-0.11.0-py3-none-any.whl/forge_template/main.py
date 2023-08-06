import logging
import sys

import click

from forge_template.actions import delete, deploy, generate
from forge_template.constants import Tools
from forge_template.sa_actions import extractor_workflow, generate_data_replication
from forge_template.user_interface import UserInterface

LOGGING_FILE = "logs.log"


GENERATE_OPTIONS = {tool.name.capitalize(): (lambda tool=tool: generate(tool)) for tool in Tools.get_values()}
DEPLOY_OPTIONS = {tool.name.capitalize(): (lambda tool=tool: deploy(tool)) for tool in Tools.get_values()}
DELETE_OPTIONS = {tool.name.capitalize(): (lambda tool=tool: delete(tool)) for tool in Tools.get_values()}
DATA_REPLICATION_OPTIONS = {
    "Set up extractor workflow": lambda: extractor_workflow(),
    "Generate custom data replication": lambda: generate_data_replication(),
}


class ForgeUI(UserInterface):
    def __init__(self):
        main_options = {
            "Generate config": lambda: self.show_menu("Which tool do you want to generate?", GENERATE_OPTIONS),
            "Deploy config": lambda: self.show_menu("Which tool do you want to deploy?", DEPLOY_OPTIONS),
            "Delete resources": lambda: self.show_menu("Which tool do you want to delete?", DELETE_OPTIONS),
            "Extractor workflow & data replication": lambda: self.show_menu(
                "What do you want to do?", DATA_REPLICATION_OPTIONS
            ),
        }

        self.print_title("Forge Template")
        logging.info("If you have any questions that are not answered by the readme, please contact Team Forge\n")
        self.show_menu("What do you want to do?", main_options, is_top_level=True)
        self.print_title("Good bye!")


@click.group(invoke_without_command=True)
def cli():
    _configure_logger()
    ForgeUI()


def _configure_logger():
    logging.basicConfig(filename=LOGGING_FILE, level=logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
