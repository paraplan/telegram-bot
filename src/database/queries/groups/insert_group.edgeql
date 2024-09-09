select (
  insert `Group` {
    full_name := <str>$full_name,
    name := <str>$name
  } unless conflict on .full_name else `Group`
) {*};
