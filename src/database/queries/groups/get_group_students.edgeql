select User { telegram_id, `group`: { full_name } } filter .`group`.id = <uuid>$group_id;
