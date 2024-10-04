update User
filter .telegram_id = <int64>$telegram_id
set {
  default_subgroup := <int16>$sub_group
};
