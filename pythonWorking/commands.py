

from config import LOG_FILE, EXPORT_FILE, DATE_FORMAT, JSON_INDENT, LINE_INDENT, SEPARATOR
from datetime import date, timedelta
from storage import load_entries, save_entries, append_entries, save_json


def log(date_str):

    work = input("오늘 한 일은?: ") or "없음"
    learn = input("배운것은?: ") or "없음"

    if work == "없음" and learn == "없음":
        message = "오늘은 아무것도 안했네요. 내일은 더 열심히 해봐요!"
    elif work == "없음" or learn == "없음":
        message = "오늘은 일부분만 했네요. 내일은 더 열심히 해봐요!"
    else:
        message = "오늘 하루도 수고 많았어요!"

    return f"""
**{date_str}**

오늘 한 일은?
 - {work}

배운것은?
 - {learn}

{message}


"""


def show_all(entries):
    if not entries:
        print("현재 로그가 없습니다.")
        return

    for entry in entries:
        print(entry.text)
        print(SEPARATOR)


def show_by_date(entries, date_str):
    for entry in entries:
        if entry.date == date_str:
            print(entry.text)
            return

    print(date_str + " 에 작성된 로그가 없습니다.")


def add_entry(date):
    entry = log(date)
    append_entries(entry)


def update(entries, date_str):
    for entry in entries:
        if entry.date == date_str:
            entry.text = log(date_str)
            save_entries(entries)
            print(f"{date_str} 로그를 수정했습니다.")
            return

    print(f"{date_str}에 작성된 로그가 없습니다.")


def delete(entries, date_str):
    position = None
    number = 0

    for entry in entries:
        if entry.date == date_str:
            position = number
        number += 1

    if position is None:
        print(f"{date_str}에 삭제할 로그가 없습니다.")
        return

    del entries[position]
    print(f"{date_str} 로그를 삭제했습니다.")
    save_entries(entries)

#SEARCH------------------------------------------------------------------------------------
def find_entries(entries, word):
    found = []
    for entry in entries:
        if word in entry.text:
            found.append(entry)
    return found


def print_entries(entries, word):
    if entries:
        for entry in entries:
            print(LINE_INDENT + entry['text'] + LINE_INDENT)
    else:
        print(f"'{word}'에 대한 검색 결과가 없습니다.")


def search(entries, keyword):
    results = find_entries(entries, keyword)
    print_entries(results, keyword)
#------------------------------------------------------------------------------------


#STATS------------------------------------------------------------------------------------
def get_date_range(entries):
    dates = [entry.date for entry in entries]
    return min(dates), max(dates)


def get_recent_entries(entries):
    today = date.today()
    day_minus_seven = today - timedelta(days=7)
    days_worked = 0
    for entry in entries:
        entry_date = date.fromisoformat(entry.date)  
        if day_minus_seven <= entry_date:
            days_worked += 1
    return days_worked


def get_top_words(entries):
    top_words = {}
    for entry in entries:
        parts = entry.text.split(LINE_INDENT)
        work = parts[1].split("\n", 1)[1].strip().lstrip("- ").strip()
        learn = parts[2].split("\n", 1)[1].strip().lstrip("- ").strip()
        work_and_learn = work + " " + learn
        words = work_and_learn.replace("\n", " ").split(" ")
        for word in words:
            word = word.strip()
            if not word:
                continue
            top_words[word] = top_words.get(word, 0) + 1
    sorted_words = sorted(top_words.items(), key=lambda item: item[1])
    top_5 = sorted_words[-5:]
    top_5 = top_5[::-1]
    return top_5


def calculate_stats(entries):
   first_date, last_date = get_date_range(entries)
   recent_entries = get_recent_entries(entries)
   top_5 = get_top_words(entries)
   return {     
	   "total": len(entries),
	   "first_date": first_date,
	   "last_date": last_date,
	   "recent_count": recent_entries,
	   "top_5": top_5
	  }


def print_stats(result):
    print(f"\n총 업무 기록: {result["total"]}건")
    print("가장 오래된 기록: " + result["first_date"])
    print("가장 최근 기록: " + result["last_date"])
    print(f"최근 7일 기록 : {result["recent_count"]}건")
    print("자주 등장한 단어:\n")
    for word, count in result["top_5"]:
        print(f"{word} ({count}번)")


def stats(entries):
	results = calculate_stats(entries)
	print_stats(results)
#------------------------------------------------------------------------------------

def export(entries):
    save_json(entries)
    print("pythonWorking.json를 Export했습니다.")

