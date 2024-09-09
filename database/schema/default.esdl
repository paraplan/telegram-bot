module default {
	type `Group` {
		required name: str;
		required full_name: str { constraint exclusive };
		students:= .<`group`[is User];
	}

	type User {
		required telegram_id: int64 { constraint exclusive };
		`group`: `Group`;
		required created_at: datetime {
			default := datetime_of_transaction();
			readonly := true;
		};
	}

	type Subject {
		required name: str { constraint exclusive };
	}

	type SeminarSchedule {
		required date: datetime;
		required `group`: `Group`;
		required multi seminars: Seminar;
	}

	type Seminar {
		cabinet: Cabinet;
		required subject: Subject;
		required sub_group: int16;
		required start_time: datetime;
		required end_time: datetime;
		required number: int16;
	}

	type Cabinet {
		required schema_id: int32 { constraint exclusive };
		required room: str;
		required name: str;
	}
}
