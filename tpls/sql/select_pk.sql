create or replace function select_{{sprocName}}(p_in {{returnType}}) returns setof {{returnType}} as
$BODY$
declare 
begin
  return query select
{{ selectColumns }}
  where
{{ whereColumns }}
  ;
end
$BODY$

language plpgsql
    volatile
    security definer
    cost 100;

