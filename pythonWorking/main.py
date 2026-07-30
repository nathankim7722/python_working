# cd "C:\Users\jaese\Desktop\programming folder\python\python_working"

from config import DATE_FORMAT, LINE_INDENT, SEPARATOR
import sys
import re
from datetime import date, datetime
from storage import load_entries, save_entries, append_entries, save_json
import commands

#COMMAND------------------------------------------------------------------------------------
def usage():
    print("""사용법:
    python main.py add/new/create
    python main.py list
    python main.py today
    python main.py date""" + DATE_FORMAT + LINE_INDENT)


def command_check(argv):
    if len(argv) <= 1:
        print(LINE_INDENT + "명령어를 입력하세요.")
        usage()
        return
    return True
#------------------------------------------------------------------


#DATE------------------------------------------------------------------------------------
def has_date(command, argv):
    if len(argv) <= 2:
        print(LINE_INDENT + f"""날짜를 입력하세요.
사용법:
  python main.py {command}""" + DATE_FORMAT + LINE_INDENT)
        return False
    return True


def date_format_check(command,argv):
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", argv[2]):
        print(LINE_INDENT + "날짜는 " + DATE_FORMAT + f""" 형식으로 입력하세요.
사용법:
  python main.py {command}""" + DATE_FORMAT + LINE_INDENT)
        return False
    return True


def date_exist_check(argv):
    try:
        date.strptime(str(argv[2]), "%Y-%m-%d")
        return True
    except ValueError:
        print(LINE_INDENT + "존재하지 않은 날짜입니다." + LINE_INDENT)
        return False


def date_all(command, argv):
    var_has_date = has_date(command, argv)

    if var_has_date == False:
        return
    else:
        var_date_format_check = date_format_check(command,argv)

    if var_date_format_check == False:
        return
    else:
        var_date_exist_check = date_exist_check(argv)

    if var_date_exist_check == False:
        return
    else:
        return argv[2]
#------------------------------------------------------------------------------------


#커맨드에 서치할 단어가가 있는지 없는지
def has_search_word(argv):
    if len(argv) <= 2:
        print(LINE_INDENT + """검색어를 입력하세요.
사용법:
  python main.py search <keyword>""" + LINE_INDENT)
        return
    return argv[2]

#오늘의 로그가 이미 있는지 없는지   
def has_entry(entries, date):
    for entry in entries:
        if entry.date == date:
            return True
    return False


def main():
    if not command_check(sys.argv):
        return

    command = sys.argv[1]
    command = command.lower()

    match command:

        case "add" | "new" | "create":
            ac = has_entry(load_entries(), str(date.today()))

            if ac == False:
                commands.add_entry(date.today())
            else:
                print(LINE_INDENT + f"""오늘({str(date.today())})의 로그를 이미 작성했습니다, 변경을 위해 업데이트 커맨드를 사용해 주세요.
예: python main.py update """ + DATE_FORMAT + LINE_INDENT)

        case "list":
            commands.show_all(load_entries())

        case "today":
            commands.show_by_date(load_entries(), str(date.today()))

        case "update":
            result = date_all(command, sys.argv)

            if result:
                commands.update(load_entries(), result)

        case "delete":
            result = date_all(command, sys.argv)

            if result:
                commands.delete(load_entries(), result)

        case "date":
            result = date_all(command, sys.argv)

            if result:
                commands.show_by_date(load_entries(), result)

        case "search":
            result = has_search_word(sys.argv)

            if result:
                commands.search(load_entries(), result)

        case "stats":
            commands.stats(load_entries())

        case "export":
            commands.export(load_entries())

        case _:
            print(LINE_INDENT + "지원하지 않는 명령어 입니다.")
            usage()


if __name__ == "__main__":
    main()