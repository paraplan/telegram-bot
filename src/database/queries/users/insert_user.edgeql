select (
  insert User {
    telegram_id := <int64>$telegram_id,
    default_subgroup := 1,
  } unless conflict on .telegram_id else User
) { ** };
