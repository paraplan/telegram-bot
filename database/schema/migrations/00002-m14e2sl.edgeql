CREATE MIGRATION m14e2slgrbezzh5rjlqptz5loktbdq3vdfxnjrljotoyn5rsdtz32q
    ONTO m1h7rbfofy6pggmt5h5oaw4kehwbqppltevs5f7zmbsuev567h6ckq
{
  ALTER TYPE default::SeminarSchedule {
      ALTER PROPERTY date {
          SET TYPE cal::local_date USING (cal::to_local_date(.date, 'Europe/Moscow'));
      };
  };
};
