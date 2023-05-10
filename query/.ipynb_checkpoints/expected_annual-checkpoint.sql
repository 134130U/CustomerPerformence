with expectation as (select a.id,a.slug,a.created_at::date as registration_date,(generate_series(a.created_at, (a.created_at+ interval  '1 month')::date + interval  '1 month'*g.month*2, '1 Month'))::date as date_at,
(a.created_at::date + interval  '1 month'*g.month) end_contract_date,user_id,g.total_amount,a.group_id,g.name as group_name,g.arrhes,g.arrhes as expect_amount,a.price_program,g.month,g.invoice_model,
case when g.id_tenant = 1 then 'Senegal'
	when g.id_tenant = 2 then 'Mali'
    when g.id_tenant = 3 then 'Nigeria'
    When g.id_tenant = 4 then 'Burkina'
    when g.id_tenant = 5 then 'Niger'
 	when g.id_tenant = 6 then 'Cameroun'
    else  'others' end as country
from accounts a
inner join(select * from groups where invoice_model=0)g
on g.id = a.group_id)
select id,slug,user_id,registration_date,date_at,to_char(date_at,'yyyy-mm') as month,total_amount,arrhes,(total_amount-arrhes) as amount_moins_deposit,group_name,country,group_id,invoice_model, expect_amount,
arrhes as cum_expect_amount
from expectation
where to_char(date_at,'yyyy-mm')<=to_char(now(),'yyyy-mm') and date_at>=end_contract_date and lower(group_name) not like '%test%'
order by id,date_at
-- limit 100