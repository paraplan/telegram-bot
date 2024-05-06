insert Cabinet {
  number := <str>$number,
  schema_id := <int16>$schema_id,
  title := <str>$title,
} unless conflict on .schema_id;
