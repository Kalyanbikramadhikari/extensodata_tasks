show databases;

show databases;

use client_rw;

show tables;
select * from fc_transaction_base;
select * from fc_account_master;

describe fc_transaction_base;
ALTER TABLE fc_transaction_base
RENAME COLUMN ï»¿tran_date to tran_date;
-- TASK 2 
select 
account_number, 
month(tran_date) as monthly,
avg(case when dc_indicator = 'deposit' then lcy_amount else null end) as average_deposit,
avg(case when dc_indicator = 'withdraw' then lcy_amount else null end) as average_withdraw,
std(case when dc_indicator = 'deposit' then lcy_amount else null end) as std_deposit,
std(case when dc_indicator = 'withdraw' then lcy_amount else null end) as std_withdraw,
variance(case when dc_indicator = 'deposit' then lcy_amount else null end) as var_deposit,
variance(case when dc_indicator = 'withdraw' then lcy_amount else null end) as var_withdraw
from fc_transaction_base 
group by account_number, monthly;

-- task 3-- 
select * from fc_account_master as am 
join fc_transaction_base as tb 
on am.account_number = tb.account_number;
Create table temp_table as
select
am.account_number, am.customer_code,
month(tran_date) as monthly,
avg(case when dc_indicator = 'deposit' then lcy_amount else null end) as average_deposit,
avg(case when dc_indicator = 'withdraw' then lcy_amount else null end) as average_withdraw,
std(case when dc_indicator = 'deposit' then lcy_amount else null end) as std_deposit,
std(case when dc_indicator = 'withdraw' then lcy_amount else null end) as std_withdraw,
variance(case when dc_indicator = 'deposit' then lcy_amount else null end) as var_deposit,
variance(case when dc_indicator = 'withdraw' then lcy_amount else null end) as var_withdraw
from fc_account_master as am 
join fc_transaction_base as tb 
on am.account_number = tb.account_number
group by am.account_number, monthly, am.customer_code;



CREATE DATABASE fc_facts;



