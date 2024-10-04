CREATE MIGRATION m13tvn4o7ls2ymkozm3tswxow3gx445nccio4acwp5dfxwbragxm3a
    ONTO m14e2slgrbezzh5rjlqptz5loktbdq3vdfxnjrljotoyn5rsdtz32q
{
  ALTER TYPE default::User {
      CREATE REQUIRED PROPERTY default_subgroup: std::int16 {
          SET REQUIRED USING (<std::int16>{1});
      };
  };
};
