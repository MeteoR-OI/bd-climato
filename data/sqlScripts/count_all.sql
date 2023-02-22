drop function if exists count_rows_of_table;

create function count_rows_of_table(
  schema    text,
  tablename text
  )
  returns   integer

  security  invoker
  language  plpgsql
as
$body$
declare
  query_template constant text not null :=
    '
      select count(*) from "?schema"."?tablename"
    ';

  query constant text not null :=
    replace(
      replace(
        query_template, '?schema', schema),
     '?tablename', tablename);

  result int not null := -1;
begin
  execute query into result;
  return result;
end;
$body$;

SELECT table_name, 
        count_rows_of_table(table_schema, table_name) AS row_count
FROM information_schema.tables
WHERE table_schema NOT IN ('pg_catalog', 'information_schema') 
    AND table_type='BASE TABLE'
    AND table_name in ('obs', 'extremes', 'histo_obs', 'histo_extreme', 'incidents')
ORDER by 1;
