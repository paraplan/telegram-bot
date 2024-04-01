insert Lesson {
  cabinet := (select Cabinet filter .schema_id = <int16>$cabinet_id),
  lecturer := (select Lecturer filter .schema_id = <int16>$lecturer_id),
};
