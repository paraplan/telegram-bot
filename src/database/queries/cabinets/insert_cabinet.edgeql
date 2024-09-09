with
  cabinet := (
    insert Cabinet {
      name := <str>$name,
      room := <str>$room,
      schema_id := <int32>$schema_id
    } unless conflict on .schema_id else Cabinet
  )

select cabinet {**};
