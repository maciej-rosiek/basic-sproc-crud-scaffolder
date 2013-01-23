create or replace function delete_{{sprocName}}(p_in {{returnType}}) returns setof {{returnType}} as
$BODY$
declare
begin
  return delete from {{schema}}.{{tableName}}
  where
{{ whereColumns }}
  returning
{{ returnColumns }}
end
$BODY$

language plpgsql
    volatile
    security definer
    cost 100;

