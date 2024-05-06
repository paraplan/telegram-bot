insert Couple {
  break_time := <int16>$break_time,
  number := <int16>$number,
  time_start := <datetime>$time_start,
  time_end := <datetime>$time_end,
  lessons := (
    select (Lesson) filter { Lesson.id in array_unpack(<array<uuid>>$lesson_ids) }
  ),
};
