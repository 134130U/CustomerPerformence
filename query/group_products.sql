select g.id as group_id,gt.name as category,case when invoice_model = 0 then 'Annual' else 'Monthly' end as payment_type
 from groups g
join system_types st on st.id=g.system_type_id
join grouprods_system_types gst on st.id=gst.system_type_id
join grouprods gt on gt.id=gst.grouprod_id
where invoice_model in(0,1)
