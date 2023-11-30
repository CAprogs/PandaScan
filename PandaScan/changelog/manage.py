import yaml
import os
import json
from datetime import datetime
from .utils import read_previous_state, generate_report
from .utils import write_current_state
from foundation.core.essentials import MAIN_DIRECTORY, SETTINGS
from foundation.core.essentials import PATH_TO_CONFIG


def generate_changelog(PATH_TO_WEBSITE, website):
    """Generate a changelog for a specific website.

    Args:
        PATH_TO_WEBSITE (str): the path to the website directory (update)
        website (str): the name of the website
    """

    with open(f'{PATH_TO_WEBSITE}/datas/mangas_chapters_temp.yml', 'r') as temp_file:
        current_state = yaml.safe_load(temp_file)

    previous_state = read_previous_state(PATH_TO_WEBSITE)
    if previous_state == {}:
        return print(f"\nNo previous state found ! | {website}")

    changelog = generate_report(current_state, previous_state)

    if changelog == "":
        changelog = "No added / deprecated files !\n"

    update_time = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")
    update_number = SETTINGS["websites"][website]["n_update"]
    update_number += 1

    report = f"\nUpdate {update_number} : {update_time}\n{changelog}"

    with open(f'{MAIN_DIRECTORY}/changelog/websites/{website}/changelog.txt', 'a') as file:
        file.write(report)

    SETTINGS["websites"][website]["n_update"] = update_number
    with open(PATH_TO_CONFIG, 'w') as json_file:
        json.dump(SETTINGS, json_file, indent=4)

    write_current_state(current_state, PATH_TO_WEBSITE)

    os.remove(f'{PATH_TO_WEBSITE}/datas/mangas_chapters_temp.yml')
