update User
filter .telegram_id = <int64>$telegram_id
set {
  `group` := (select `Group` filter .id = <uuid>$group_id)
};
