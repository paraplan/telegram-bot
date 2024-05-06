CREATE MIGRATION m1m77wwpiy5rp55wejiqjdpjqmyk5muyr4czmw4e7b67p2npxs7f4q
    ONTO initial
{
  CREATE ABSTRACT TYPE default::BaseItem {
      CREATE REQUIRED PROPERTY full_name: std::str;
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE REQUIRED PROPERTY schema_id: std::int16 {
          CREATE CONSTRAINT std::exclusive;
      };
  };
  CREATE TYPE default::`Group` EXTENDING default::BaseItem;
  CREATE TYPE default::Lecturer EXTENDING default::BaseItem;
  CREATE TYPE default::Cabinet {
      CREATE REQUIRED PROPERTY number: std::str;
      CREATE REQUIRED PROPERTY schema_id: std::int16 {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY title: std::str;
  };
  CREATE TYPE default::Lesson {
      CREATE LINK cabinet: default::Cabinet;
      CREATE LINK lecturer: default::Lecturer;
  };
  CREATE TYPE default::Couple {
      CREATE MULTI LINK lessons: default::Lesson;
      CREATE PROPERTY break_time: std::int16;
      CREATE REQUIRED PROPERTY number: std::int16;
      CREATE PROPERTY time_end: std::datetime;
      CREATE PROPERTY time_start: std::datetime;
  };
  CREATE TYPE default::StudyDay {
      CREATE MULTI LINK couples: default::Couple;
      CREATE REQUIRED LINK `group`: default::`Group`;
      CREATE REQUIRED PROPERTY date: std::datetime;
  };
  CREATE TYPE default::User {
      CREATE LINK `group`: default::`Group`;
      CREATE REQUIRED PROPERTY created_at := (std::datetime_of_transaction());
      CREATE REQUIRED PROPERTY telegram_id: std::int64 {
          CREATE CONSTRAINT std::exclusive;
      };
  };
  ALTER TYPE default::`Group` {
      CREATE MULTI LINK students: default::User;
  };
};
