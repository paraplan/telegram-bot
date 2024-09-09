select (
  insert User {
    telegram_id := <int64>$telegram_id
  } unless conflict on .telegram_id else User
) { ** };
