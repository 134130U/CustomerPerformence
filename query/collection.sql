select slug,to_char(p.created_at,'yyyy-mm') as month,sum(amount) as amount_paid,rank() over (partition by slug order by to_char(p.created_at,'yyyy-mm')) as ranked_month
from payments p
inner join accounts a on a.slug = p.account_slug
where invoice_model in(0,1) and is_cancel is False and amount>0 and p.created_at::date != a.created_at::date
group by 1,2