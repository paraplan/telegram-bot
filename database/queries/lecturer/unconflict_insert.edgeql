insert Lecturer {
  schema_id := <int16>$schema_id,
  name := <str>$name,
  full_name := <str>$full_name,
} unless conflict on .schema_id;
