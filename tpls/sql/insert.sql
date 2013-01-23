create or replace function insert_{{sprocName}}(p_in {{returnType}}) returns setof {{returnType}} as
$BODY$
declare 
  return query insert into {{schema}}.{{tableName}} (
{{columns}}
  )
  select
{{ insertValues }}
  returning
{{ returnColumns }}
end
$BODY$

language plpgsql
    volatile
    security definer
    cost 100;

