select SeminarSchedule { id, date, `group`: { * }, seminars: { ** } }
filter (
  .`group`.id = <uuid>$group_id and
  .date = <cal::local_date>$date
) limit 1;
