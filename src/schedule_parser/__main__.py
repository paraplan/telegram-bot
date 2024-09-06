import orjson

from src.schedule_parser.study_day import StudyDay

with open("schedule.json") as file:
    text = file.read()
# print(orjson.loads(text))
schedule = StudyDay(**orjson.loads(text))
print(schedule)
