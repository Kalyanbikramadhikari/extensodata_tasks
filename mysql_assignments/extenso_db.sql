
create database extensodata;-- 
show databases;
use extensodata;
show tables;
select * from product_category_map;
select * from rw_transaction_data;
ALTER TABLE rw_transaction_data ADD yearmonth VARCHAR(7);-- 
select * from rw_transaction_data;
alter TABLE rw_transaction_data DROP column yearmonth ;-- 

-- CREATE TABLE combined__rw_and_map AS
-- select rw_transaction_data.*, product_category_map.*
-- from rw_transaction_data
-- INNER JOIN product_category_map on rw_transaction_data.module_id = product_category_map.module_id 
-- AND rw_transaction_data.product_id = product_category_map.product_id
-- AND rw_transaction_data.product_type_id = product_category_map.product_type_id;
CREATE TABLE combined_rw_and_map AS
SELECT *
FROM rw_transaction_data
INNER JOIN product_category_map 
USING (module_id, product_id, product_type_id);

select * from combined_rw_and_map;


SET SQL_SAFE_UPDATES = 0;
alter table combined_rw_and_map add column Months int;
update combined_rw_and_map
set Months = month(last_modified_date);


--  functionality of pivot table

	SELECT payer_account_id, Months, 
		SUM(CASE WHEN txn_flow = 'Value Chain' THEN amount ELSE 0 END) AS Value_chain,
        SUM(CASE WHEN txn_flow = 'OutFlow' THEN amount ELSE 0 END) AS OutFlow,
		SUM(CASE WHEN txn_flow = 'InFlow' THEN amount ELSE 0 END) AS InFlow
        
	FROM combined_rw_and_map
	GROUP BY payer_account_id;


-- creating new table that will have 9 columns of the final table 
CREATE TABLE if not exists expected_table  AS
SELECT payer_account_id,
		sum(reward_point) as total_reward_point,
        max(last_modified_date) as last_modified_date,
        product_name as latest_used_product,
        sum(revenue_amount) as Total_revenue,
        avg(revenue_amount) as Monthly_revenue,
		SUM(CASE WHEN txn_flow = 'Value Chain' THEN amount ELSE 0 END) AS Total_Value_chain,
        SUM(CASE WHEN txn_flow = 'OutFlow' THEN amount ELSE 0 END) AS Total_OutFlow,
		SUM(CASE WHEN txn_flow = 'InFlow' THEN amount ELSE 0 END) AS Total_InFlow,
        COUNT(CASE WHEN txn_flow = 'Value Chain' THEN amount ELSE null END) AS Total_Value_chain_count,
        COUNT(CASE WHEN txn_flow = 'OutFlow' THEN amount ELSE null END) AS Total_OutFlow_count,
		COUNT(CASE WHEN txn_flow = 'InFlow' THEN amount ELSE null END) AS Total_InFlow_count,
--         SUM(CASE WHEN txn_flow = 'OutFlow' THEN amount ELSE null END) AS Total_OutFlow,
		AVG(CASE WHEN txn_flow = 'Value Chain' THEN amount ELSE null END) AS Monthly_Total_Value_chain,
        AVG(CASE WHEN txn_flow = 'OutFlow' THEN amount ELSE null END) AS Monthly_Total_OutFlow,
		AVG(CASE WHEN txn_flow = 'InFlow' THEN amount ELSE null END) AS Monthly_Total_InFlow
        
        FROM combined_rw_and_map
		GROUP BY payer_account_id;
        
        select * from expected_table;
       
       
--  reward point for each product_id. This will be the total reward point
-- select payer_account_id, 
-- 	   sum(reward_point)
-- 	   from combined_rw_and_map
--        group by payer_account_id;


create table most_used_pr as
select payer_account_id,product_name,cnt from(
select payer_account_id ,product_name,
count(product_name) over(partition by payer_account_id,product_name) as cnt
 from combined_rw_and_map) sub
group by payer_account_id,product_name order by payer_account_id desc,cnt desc;

select * from most_used_pr;

create table most_used_prod as
select * ,row_number() over(partition by payer_account_id order by cnt desc) as row_num from most_used_pr;
select * from most_used_prod;

drop table most_used_product;
create table most_used_product as
select payer_account_id,product_name as most_used_product from most_used_prod where row_num=1;

drop table second_used_product;
create table second_used_product as
select payer_account_id,product_name as second_most_used_prod from most_used_prod where row_num=2;

drop table third_used_product;
create table third_used_product as
select payer_account_id,product_name as third_most_used_prod from most_used_prod where row_num=3;


create table final_table as
select * from expected_table
left join most_used_product using (payer_account_id)
left join second_used_product using (payer_account_id)
left join third_used_product using (payer_account_id);

select * from final_table;
       

    
    
    

       
       
       
        

        
        


 













