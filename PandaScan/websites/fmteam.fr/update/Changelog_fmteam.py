import yaml
from Path_to_fmteam import script_repo

def read_previous_state():
    """Read the previous state of the mangas chapters.

    Returns:
        _type_: dict
    """
    try:
        with open(f'{script_repo}/datas/mangas_chapters.yml', 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        return {}

def write_current_state(state):
    """Write the current state of the mangas chapters.

    Args:
        state (_type_): The current state of the mangas chapters.
    """    
    with open(f'{script_repo}/datas/mangas_chapters.yml', 'w') as file:
        yaml.dump(state, file)

def read_update_number():
    """Read the update number.

    Returns:
        _type_: int
    """    
    try:
        with open(f'{script_repo}/changelog/update_number.txt', 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def write_update_number(number):
    """Write the update number.

    Args:
        number (_type_): The update number.
    """    
    with open(f'{script_repo}/changelog/update_number.txt', 'w') as file:
        file.write(str(number))

def generate_change_report(current_state, previous_state):
    """Generate the change report.

    Args:
        current_state (_type_): the current state of the mangas chapters.
        previous_state (_type_): the previous state of the mangas chapters.

    Returns:
        _type_: str
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

def generate_changelog():
    """Generate the changelog.
    """
    from datetime import datetime
    import os

    # Load the temporary YAML file
    with open(f'{script_repo}/datas/mangas_chapters_temp.yml', 'r') as temp_file:
        current_state = yaml.safe_load(temp_file)

    previous_state = read_previous_state()

    change_report = generate_change_report(current_state, previous_state)

    if change_report == "":
        change_report = "No added / deprecated files !\n"

    update_time = datetime.now().strftime("%d/%m/%Y | %H:%M:%S")

    update_number = read_update_number()  
    if os.path.exists(f'{script_repo}/changelog/update_number.txt'):
        update_number += 1 

    report = f"\nUpdate {update_number} : {update_time}\n{change_report}"

    with open(f'{script_repo}/changelog/changelog.txt', 'a') as file:
        file.write(report)

    write_update_number(update_number)
    write_current_state(current_state)

    # Remove the temporary YAML file
    os.remove(f'{script_repo}/datas/mangas_chapters_temp.yml')



# Uncomment to debug
#if __name__ == "__main__":
    #generate_changelog()