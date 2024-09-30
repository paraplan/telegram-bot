select SeminarSchedule {
  seminars: { id } order by .id
}
filter .`group`.id = <uuid>$group_id
and .date = <cal::local_date>$date
limit 1;
