

from config import LOG_FILE, EXPORT_FILE, DATE_FORMAT, JSON_INDENT, LINE_INDENT, ENTRY_SEPARATOR
import json
from dataclasses import dataclass, asdict


@dataclass
class WorkLogEntry:
    date: str
    text: str 


def load_entries():
    entries = []

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        return entries

    raw_entries = content.strip().split(ENTRY_SEPARATOR)

    for raw in raw_entries:
        raw = raw.strip()

        if not raw:
            continue

        first_line = raw.split("\n")[0]
        date = first_line.replace("*", "").strip()
        entries.append(WorkLogEntry(date, raw))

    return entries


def save_entries(entries):
    with open(LOG_FILE, "w", encoding="utf-8") as file:
        if entries:
            file.write(
                ENTRY_SEPARATOR.join(entry.text for entry in entries)
                + ENTRY_SEPARATOR
            )
        else:
            file.write("")


def append_entries(entry):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(entry)


def load_json():
    entries = []

    try:
        with open(EXPORT_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return entries

    entries = [WorkLogEntry(**e) for e in data]
    return entries


def save_json(entries):
    list_of_json = []
    for e in entries:
        dict = asdict(e)
        list_of_json.append(dict)
        with open(EXPORT_FILE, "w", encoding="utf-8") as file:
            json.dump(list_of_json, file, ensure_ascii=False, indent=JSON_INDENT)

