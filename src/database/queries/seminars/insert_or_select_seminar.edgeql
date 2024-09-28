WITH
  cabinet := (
    SELECT Cabinet
    FILTER .schema_id = <optional int32>$cabinet_schema_id
  ),
  subject := (
    SELECT Subject
    FILTER .name = <str>$subject_name
  ),
  seminar := (
    SELECT Seminar
    FILTER
      (IF EXISTS <optional int32>$cabinet_schema_id THEN .cabinet = cabinet ELSE TRUE) AND
      .subject = subject AND
      .sub_group = <int16>$sub_group AND
      .start_time = <datetime>$start_time AND
      .end_time = <datetime>$end_time AND
      .number = <int16>$number
  )

SELECT (
  IF EXISTS seminar THEN
    seminar
  ELSE (
    INSERT Seminar {
      cabinet := cabinet IF EXISTS <optional int32>$cabinet_schema_id ELSE {},
      subject := subject,
      sub_group := <int16>$sub_group,
      start_time := <datetime>$start_time,
      end_time := <datetime>$end_time,
      number := <int16>$number,
    }
  )
) { ** };
