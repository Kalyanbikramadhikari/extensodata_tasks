show databases;
CREATE DATABASE ;
show databases;
use client_rw;
select * from fc_transaction_base;

describe fc_transaction_base;


SELECT account_number , month(ï»¿tran_date),
avg(case when dc_indicator='deposit' then lcy_amount else null end ) as average_deposit ,
avg(case when dc_indicator='withdraw' then lcy_amount else null end) as average_withdraw,
std(case when dc_indicator='withdraw' then lcy_amount else null end) as standarddeviation_withdraw,
std(case when dc_indicator='deposit' then lcy_amount else null end) as standarddeviation_deposit,
variance(case when dc_indicator='withdraw' then lcy_amount else null end) as variance_withdraw,
variance(case when dc_indicator='deposit' then lcy_amount else null end) as variance_deposit 
FROM fc_transaction_base 
group by account_number, month(ï»¿tran_date);







