import re
from datetime import date

LOG_FILE = "workLogFinal.md"


def loadEntries():
    entries = []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return entries

    rawEntries = content.strip().split("\n\n\n")
    for raw in rawEntries:
        raw = raw.strip()
        if not raw:
            continue
        first_line = raw.split("\n")[0]
        date_str = first_line.replace("*", "").strip()
        entries.append({"date": date_str, "text": raw})
    return entries


def showAll(entries):
    if not entries:
        print("현재 로그가 없습니다.")
        return
    for e in entries:
        print(e["text"])
        print("\n" + "-" * 30 + "\n")


def showByDate(entries, dateStr):
    for e in entries:
        if e["date"] == dateStr:
            print(e["text"])
            return
    print(dateStr + " 에 작성된 로그가 없습니다.")


def log(dateStr):

    work = input("오늘 한 일은?: ") or "없음"
    learn = input("배운것은?: ") or "없음"

    if work == "없음" and learn == "없음":
        message = "오늘은 아무것도 안했네요. 내일은 더 열심히 해봐요!"
    elif work == "없음" or learn == "없음":
        message = "오늘은 일부분만 했네요. 내일은 더 열심히 해봐요!"
    else:
        message = "오늘 하루도 수고 많았어요!"

    return f"""**{dateStr}**

오늘 한 일은?
 - {work}

배운것은?
 - {learn}

{message}


"""


def addEntry():
    entry = log(str(date.today()))
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(entry)


def update(entries, dateStr):
    dateStr = dateStr.split(":", 1)[1].strip()

    for e in entries:
        if e["date"] == dateStr:
            e["text"] = log(dateStr)
            
            with open(LOG_FILE, "w", encoding="utf-8") as file:
                file.write("\n\n\n".join(x["text"] for x in entries) + "\n\n\n")

            print(f"{dateStr} 로그를 수정했습니다.")
            return

    print(f"{dateStr}에 작성된 로그가 없습니다.")


def delete(entries, dateStr):
    dateStr = dateStr.split(":", 1)[1].strip()

    position = None
    num = 0

    for e in entries:
        if e["date"] == dateStr:
            position = num
        num+=1

    if position is None:
        print(f"{dateStr}에 삭제할 로그가 없습니다.")
        return
    
    del entries[position]
    print(f"{dateStr} 로그를 삭제했습니다.")

    with open(LOG_FILE, "w", encoding="utf-8") as file:
        if entries:
            file.write("\n\n\n".join(e["text"] for e in entries) + "\n\n\n")
        else:
            file.write("")




def main():
    command = input("명령어를 입력하세요 (list / today / YYYY-MM-D / update: YYYY-MM-DD / delete: YYYY-MM-DD), 새 로그 작성은 Enter: ").strip()

    if command == "list" or command == "List":
        showAll(loadEntries())
    elif command == "today" or command == "Today":
        showByDate(loadEntries(), str(date.today()))
    elif re.match(r"^update:\s*\d{4}-\d{2}-\d{2}$",command):
        update(loadEntries(), command)
    elif re.match(r"^delete:\s*\d{4}-\d{2}-\d{2}$",command):
        delete(loadEntries(), command)
    elif re.match(r"^\d{4}-\d{2}-\d{2}$", command):
        showByDate(loadEntries(), command)
    else:
        addEntry()


if __name__ == "__main__":
    main()





