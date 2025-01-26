import orjson

from src.schedule_parser.study_day import StudyDaySchema

with open("schedule.json") as file:
    text = file.read()
schedule = StudyDaySchema(**orjson.loads(text))
