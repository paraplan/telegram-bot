WITH
  group_obj := (
    SELECT `Group`
    FILTER .id = <uuid>$group_id
  ),
  seminars := (
    SELECT Seminar
    FILTER .id IN array_unpack(<array<uuid>>$seminar_ids)
  ),
  schedule := (
    SELECT SeminarSchedule
    FILTER
      .`group` = group_obj AND
      .date = <datetime>$date
  )

SELECT (
  IF EXISTS schedule THEN
    (
      UPDATE SeminarSchedule
      FILTER .id = schedule.id
      SET {
        seminars := seminars,
      }
    )
  ELSE (
    INSERT SeminarSchedule {
      `group` := group_obj,
      seminars := seminars,
      date := <datetime>$date,
    }
  )
) { ** };
