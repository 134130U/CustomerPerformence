select slug,to_char(generate_series((a.created_at+ interval  '1 month')::date,a.created_at::date + interval  '1 month'*(g.month*2),'1 month'),'yyyy-mm') as month
--,rank() over (partition by slug order by to_char(generate_series((a.created_at+ interval  '1 month')::date,a.created_at::date + interval  '1 month'*(g.month+6),'1 month'),'yyyy-mm')) as ranked_month
from accounts as a
inner join groups g on g.id=a.group_id 
where g.invoice_model in(0,1)