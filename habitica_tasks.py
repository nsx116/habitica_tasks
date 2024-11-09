from pathlib import Path
import json
import textwrap
from collections import defaultdict
from datetime import datetime

# Load file to variable
def load_file_to_variable(habitica_data_file):
    path = Path(habitica_data_file)
    contents = path.read_text()
    habitica_data = json.loads(contents)
    return habitica_data

############### Dailys ########################
def remove_duplicate_dates(habitica_data): 
    for daily in habitica_data["tasks"]["dailys"]:
        for date in daily["history"]:
            # Timestamp in milliseconds
            timestamp_ms = date["date"]
            # Convert to seconds
            timestamp_s = timestamp_ms / 1000
            # Convert to datetime object
            date_time_obj = datetime.fromtimestamp(timestamp_s)
            date_str = date_time_obj.strftime("%Y-%m-%d")
            time_str = date_time_obj.strftime("%H:%M")
            date["date"] = date_str
            date["time"] = time_str

        history = daily['history']
        unique_history = {}
        for entry in history:
            unique_history[entry["date"]] = entry

        daily['history'] = list(unique_history.values())

    return habitica_data


def make_dailys_by_date_dict(habitica_data):
    dailys_by_date = defaultdict(dict)
    for daily in habitica_data["tasks"]["dailys"]:
        for date in daily["history"]:
            text = daily["text"]
            date_str = date["date"]
            time_str = date["time"]
            try:
                completed = date["completed"]
            except KeyError:
                completed = False

            if date_str not in dailys_by_date:
                dailys_by_date[date_str] = {}

            if "dailys" not in dailys_by_date[date_str]:
                dailys_by_date[date_str]["dailys"] = []

            
            dailys_by_date[date_str]["dailys"].append((text, completed, time_str))
            dailys_by_date = dict(sorted(dailys_by_date.items()))
            # print(dailys_by_date)

    return dailys_by_date


def write_dailys_to_file(dailys_by_date):
    with open("dailys.md", "w") as file:
        for date, dailys in dailys_by_date.items():
            file.write("\n")
            file.write(date)
            file.write("\n")
            for text, completed, time_str in dailys["dailys"]:
                status = "- [x]" if completed else "- [ ]"
                file.write(f"  {status} {time_str} {text}\n")


def dailys(habitica_data_file):
    habitica_data = load_file_to_variable(habitica_data_file)
    habitica_data = remove_duplicate_dates(habitica_data)
    dailys_by_date = make_dailys_by_date_dict(habitica_data)
    write_dailys_to_file(dailys_by_date)


############### Todos  ########################
def make_todos_by_date_dict(habitica_data):
    todos_by_date = defaultdict(dict)
    for todo in habitica_data["tasks"]["todos"]:
        try:
            datetime_obj = datetime.fromisoformat(todo["date"].replace("Z", ""))  # Convert to datetime object
        except AttributeError:
            pass
        date_str = datetime_obj.strftime("%Y-%m-%d")
        time_str = datetime_obj.strftime("%H:%M")
        text = todo["text"]
        completed = todo["completed"]

        if date_str not in todos_by_date:
            todos_by_date[date_str] = {}

        if "todos" not in todos_by_date[date_str]:
            todos_by_date[date_str]["todos"] = []

        subtasks = []
        if todo["checklist"]:
            for subtask in todo["checklist"]:
                sub_text = subtask["text"]
                sub_completed = subtask["completed"]
                subtasks.append((sub_text, sub_completed))

        if date_str not in todos_by_date:
            todos_by_date[date_str] = {}

        if "todos" not in todos_by_date[date_str]:
            todos_by_date[date_str]["todos"] = []

        todos_by_date[date_str]["todos"].append({
            "text": text, 
            "completed": completed, 
            "time_str": time_str,
            "subtasks": subtasks
        })

        todos_by_date = dict(sorted(todos_by_date.items()))
    return (todos_by_date)


def write_todos_to_file(todos_by_date):
    with open("todos.md", "w") as file:
        try:
            for date, tasks in todos_by_date.items():
                file.write("\n")
                file.write(f"{date}\n")
                for text, completed, time_str in tasks['todos']:
                    status = "- [x]" if completed else "- [ ]"
                    file.write(f"  {status} {time_str} {text}\n")
        except ValueError:
            print(f"Data missing for {text}")


def todos(habitica_data_file):
    habitica_data = load_file_to_variable(habitica_data_file)
    todos_by_date = make_todos_by_date_dict(habitica_data)
    write_todos_to_file(todos_by_date)


############### All Tasks ######################

def merge_dailys_todos_into_tasks(dailys, todos):
    tasks = {}
    for date, data in dailys.items():
        tasks[date] = data

    # Merge `todos` into `tasks`
    for date, data in todos.items():
        if date in tasks:
            tasks[date].update(data)  # Add `todos` key to the existing entry
        else:
            tasks[date] = data  # Add new entry if date does not exist in `tasks`

    return tasks

def filter_by_year_and_month(tasks, year, month):
    # Ensure month is a zero-padded string
    month = str(month).zfill(2)
    # Filter items by specified year and month
    filtered_tasks = {
        date: data for date, data in tasks.items()
        if date.split("-")[0] == str(year) and date.split("-")[1] == month
    }
    return filtered_tasks

def write_tasks_to_file(tasks):
    with open("tasks.md", "w") as file:
        for date, tasks in tasks.items():
            file.write("\n")
            file.write(f"{date}\n")
            try:
                if tasks["dailys"]:
                    file.write("  Dailys:\n")
                for text, completed, time_str in tasks['dailys']:
                    status = "- [x]" if completed else "- [ ]"
                    line = f"{status} {time_str} {text}"
                    wrapped_line = textwrap.fill(line, width=75, subsequent_indent=" " * 8)
                    file.write(f"    {wrapped_line}\n")
            except KeyError:
                pass
            try:
                if tasks["todos"]:
                    file.write("  Todos:\n")
                for todo in tasks['todos']:
                    text = todo["text"]
                    completed = todo["completed"]
                    time_str = todo["time_str"]
                    subtasks = todo["subtasks"]
                    status = "- [x]" if completed else "- [ ]"

                    line = f"{status} {text}"
                    wrapped_line = textwrap.fill(line, width=75, subsequent_indent=" " * 8)
                    file.write(f"    {wrapped_line}\n")

                    if subtasks:
                        for sub_text, sub_status in subtasks:
                            sub_status_str = "- [x]" if sub_status else "- [ ]"
                            file.write(f"        {sub_status_str} {sub_text}\n")
            except KeyError:
                pass

def merge_and_write(habitica_data_file):
    habitica_data = load_file_to_variable(habitica_data_file)
    todos_by_date = make_todos_by_date_dict(habitica_data)
    habitica_data = remove_duplicate_dates(habitica_data)
    dailys_by_date = make_dailys_by_date_dict(habitica_data)
    tasks = merge_dailys_todos_into_tasks(dailys_by_date, todos_by_date)
    # tasks = filter_by_year_and_month(tasks, 2024, 11)
    write_tasks_to_file(tasks)


def main():
    habitica_data_file = 'habitica-user-data.json'
    merge_and_write(habitica_data_file)
    # dailys(habitica_data_file)
    # todos(habitica_data_file)


if __name__ == "__main__":
    main()
