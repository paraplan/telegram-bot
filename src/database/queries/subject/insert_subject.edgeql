with
  subject := (
    insert Subject {
      name := <str>$name,
    } unless conflict on .name else Subject
  )

select subject {**};
