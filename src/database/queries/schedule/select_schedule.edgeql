WITH
  `group` := (
    SELECT `Group`
    FILTER .id = <uuid>$group_id
  ),
  seminars := (
    SELECT Seminar
    FILTER .id = array_unpack(<array<uuid>>$seminar_ids)
  ),
  schedule := (
    SELECT SeminarSchedule
    FILTER
      .`group` = `group` AND
      .seminars = seminars AND
      .date = <datetime>$date
  )

SELECT (
  schedule
) { ** };
