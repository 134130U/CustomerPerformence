with expectation as (select *,(case when registration_date = date_at then arrhes
     					when invoice_model=0 and date_at != registration_date+interval'1 year' then 0 else price_program end) as expect_amount 
					 	from (select a.id,a.slug,a.created_at::date as registration_date,(generate_series(a.created_at, (a.created_at+ interval  '1 month')::date + interval  '1 month'*g.month*3, '1 Month'))::date as date_at,
(a.created_at::date + interval  '1 month'*g.month) end_contract_date,user_id,g.total_amount,a.group_id,g.name as group_name,g.arrhes,a.price_program,g.month,g.invoice_model,
case when g.id_tenant = 1 then 'Senegal'
	when g.id_tenant = 2 then 'Mali'
    when g.id_tenant = 3 then 'Nigeria'
    When g.id_tenant = 4 then 'Burkina'
    when g.id_tenant = 5 then 'Niger'
 	when g.id_tenant = 6 then 'Cameroun'
    else  'others' end as country
from accounts a
inner join(select * from groups where invoice_model=1)g
on g.id = a.group_id)tab)
select id,slug,user_id,registration_date,date_at,to_char(date_at,'yyyy-mm') as month,total_amount,arrhes,(total_amount-arrhes) as amount_moins_deposit,group_name,country,group_id,invoice_model,expect_amount,
sum(expect_amount) over (partition by id,slug order by id,slug,date_at asc rows between unbounded preceding and current row) as cum_expect_amount
from expectation
where to_char(date_at,'yyyy-mm')<=to_char(now(),'yyyy-mm') and date_at!=registration_date and lower(group_name) not like '%test%'
--expect_amount!=0 and 
order by id,date_at
