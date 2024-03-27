module default {
    abstract type BaseItem {
        required schema_id: int16 { constraint exclusive };
        required name: str;
        required full_name: str;
    }

    type User {
        required telegram_id: int64 { constraint exclusive };
        required created_at := datetime_of_transaction();
        `group`: `Group`;
    }

    type `Group` extending BaseItem {
        multi students: User;
    }

    type Lecturer extending BaseItem {}

    type Cabinet {
        required schema_id: int16 { constraint exclusive };
        required number: str;
        required title: str;
    }

    type Lesson {
        cabinet: Cabinet;
        lecturer: Lecturer;
    }

    type Couple {
        required number: int16;
        multi lessons: Lesson;
        time_start: datetime;
        time_end: datetime;
        break_time: int16;
    }

    type StudyDay {
        multi couples: Couple;
        required date: datetime;
        required `group`: `Group`;
    }
}
