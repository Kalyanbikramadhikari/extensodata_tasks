show databases;
use transaction_data;

show tables;
select * from transaction_summary;

select * from transaction_summary where TRANSACTION_DETAILS LIKE '%SALARY%' ; 