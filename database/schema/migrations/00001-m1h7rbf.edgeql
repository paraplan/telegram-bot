CREATE MIGRATION m1h7rbfofy6pggmt5h5oaw4kehwbqppltevs5f7zmbsuev567h6ckq
    ONTO initial
{
  CREATE TYPE default::Cabinet {
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE REQUIRED PROPERTY room: std::str;
      CREATE REQUIRED PROPERTY schema_id: std::int32 {
          CREATE CONSTRAINT std::exclusive;
      };
  };
  CREATE TYPE default::Subject {
      CREATE REQUIRED PROPERTY name: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
  };
  CREATE TYPE default::Seminar {
      CREATE LINK cabinet: default::Cabinet;
      CREATE REQUIRED LINK subject: default::Subject;
      CREATE REQUIRED PROPERTY end_time: std::datetime;
      CREATE REQUIRED PROPERTY number: std::int16;
      CREATE REQUIRED PROPERTY start_time: std::datetime;
      CREATE REQUIRED PROPERTY sub_group: std::int16;
  };
  CREATE TYPE default::`Group` {
      CREATE REQUIRED PROPERTY full_name: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY name: std::str;
  };
  CREATE TYPE default::User {
      CREATE LINK `group`: default::`Group`;
      CREATE REQUIRED PROPERTY created_at: std::datetime {
          SET default := (std::datetime_of_transaction());
          SET readonly := true;
      };
      CREATE REQUIRED PROPERTY telegram_id: std::int64 {
          CREATE CONSTRAINT std::exclusive;
      };
  };
  ALTER TYPE default::`Group` {
      CREATE LINK students := (.<`group`[IS default::User]);
  };
  CREATE TYPE default::SeminarSchedule {
      CREATE REQUIRED LINK `group`: default::`Group`;
      CREATE REQUIRED MULTI LINK seminars: default::Seminar;
      CREATE REQUIRED PROPERTY date: std::datetime;
  };
};
