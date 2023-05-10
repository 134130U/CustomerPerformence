select a.slug,commune,region, concat(first_name,' ',last_name) as agent,username from account_analytics a
join users u on u.id=a.user_id
