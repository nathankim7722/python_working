from datetime import datetime

date = datetime.today()

print("오늘 한 일은?: ")
work=input()
if work == "":
    work="없음"

print("배운것은?")
learn=input()
if learn == "":
    learn="없음"

with open("workLogA.md", "a", encoding="utf-8") as file:

    file.write(f"""**{date.today()}**

    오늘 한 일은?
     - {work}

    배운것은?
     - {learn}


    """)

    if work=="없음" and learn=="없음":
       file.write("오늘은 아무것도 안했네요. 내일은 더 열심히 해봐요!")
       file.write("\n\n\n")

    elif work=="없음" or learn=="없음":
       file.write("오늘은 일부분만 했네요. 내일은 더 열심히 해봐요!")
       file.write("\n\n\n")

    else:
       file.write("오늘 하루도 수고 많았어요!")
       file.write("\n\n\n")


        



