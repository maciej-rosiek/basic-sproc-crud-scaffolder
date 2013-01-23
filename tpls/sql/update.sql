create or replace function update_{{sprocName}}(p_in {{returnType}}) returns setof {{returnType}} as
$BODY$
declare 
begin
  return query update {{schema}}.{{tableName}} 
  set
{{ updateColumns }}
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

