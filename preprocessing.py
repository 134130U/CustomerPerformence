import pandas as pd
import numpy as np
import collect

collect.get_data()

df_annual = pd.read_csv('Data/annual.csv')
df_mois  = pd.read_csv('Data/monthly.csv')
df_paid = pd.read_csv('Data/payments.csv')
df_zone = pd.read_csv('Data/zones.csv')
df_prod = pd.read_csv('Data/group_products.csv')

df_expected = pd.concat([df_mois,df_annual],ignore_index=True)
df_expected['total_expect_amount'] = np.where(df_expected['cum_expect_amount']>df_expected['amount_moins_deposit'],df_expected['amount_moins_deposit'],df_expected['cum_expect_amount'])
df_paid = df_paid.sort_values(by='month')
df_paid['total_paid'] = df_paid.groupby('slug')['amount_paid'].cumsum()
df_paid['month_index'] = df_paid['ranked_month'].apply(lambda t: 'M-'+str(t))
df1  = pd.merge(df_expected,df_paid,on=['slug','month'],how='left')
df1['registration_date'] = pd.to_datetime(df1['registration_date'], errors='coerce')
df1["date_at"] = pd.to_datetime(df1["date_at"], errors='coerce')

df1['reg_month'] = df1['registration_date'].apply(lambda t: t.strftime("%Y-%m"))
data = pd.merge(df1,df_zone,on='slug',how='inner')
data = pd.merge(data,df_prod,on='group_id',how='inner')
data.to_csv('Data/finale_data.csv',index=False)