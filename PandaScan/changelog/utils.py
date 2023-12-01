import yaml


def read_previous_state(PATH_TO_WEBSITE):
    """Read the previous state of the mangas chapters.

    Args:
        PATH_TO_WEBSITE (str): path to the website folder (update module)

    Returns:
        A yaml file or an empty dict
    """
    try:
        with open(f'{PATH_TO_WEBSITE}/datas/mangas_chapters.yml', 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        return {}


def write_current_state(state, PATH_TO_WEBSITE):
    """Write the current state of the manga chapters.

    Args:
        state (Any): the current yaml file
        PATH_TO_WEBSITE (str): path to the website folder (update module)
    """
    with open(f'{PATH_TO_WEBSITE}/datas/mangas_chapters.yml', 'w') as file:
        yaml.dump(state, file)


def generate_report(current_state, previous_state):
    """Generate the changelog comparing the differences beetween current and previous state.

    Args:
        current_state (Any): the current state of the yaml file. (chapters per manga)
        previous_state (Any): the previous state of the yaml file. (chapters per manga)

    Returns:
        A changelog in string format
    """
    change_report = []

    for key in current_state:
        if key in previous_state:
            added_chapters = [chap for chap in current_state[key] if chap not in previous_state[key]]
            removed_chapters = [chap for chap in previous_state[key] if chap not in current_state[key]]
            if added_chapters or removed_chapters:
                change_report.append(f"Changes in {key}:\n")
                if added_chapters:
                    change_report.append(f"  • Added chapters: {', '.join(added_chapters)}\n")
                if removed_chapters:
                    change_report.append(f"  • Removed chapters: {', '.join(removed_chapters)}\n")
        else:
            change_report.append(f"=> Added new entry '{key}' with chapters: {', '.join(current_state[key])}\n")

    deprecated_keys = [key for key in previous_state if key not in current_state]
    if deprecated_keys:
        change_report.append("Deprecated entries:\n")
        for key in deprecated_keys:
            change_report.append(f"  • {key}: {', '.join(previous_state[key])}\n")

    return "".join(change_report)
