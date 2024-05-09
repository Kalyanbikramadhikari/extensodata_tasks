show databases;
use fc_facts;
show tables;

create database transaction_data;
use transaction_data;



SHOW VARIABLES LIKE "secure_file_priv"; 

create table transaction_summary(
    Account_No VARCHAR(255),
    Date DATE,
    TRANSACTION_DETAILS VARCHAR(255),
    CHQ_NO VARCHAR(255),
    VALUE_DATE VARCHAR(255),
    WITHDRAWAL_AMT DECIMAL(20, 2),
    DEPOSIT_AMT DECIMAL(20, 2)
    );
drop table transaction_summary;


LOAD DATA INFILE 'E:/internship-f1soft/day-3 assignment/assignment_2/encoded-transaction_summary.csv'
INTO TABLE transaction_summary
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

select * from transaction_summary;

ALTER TABLE transaction_summary
add TOTAL_BALANCE DECIMAL(20,2);

SELECT * FROM transaction_summary;

-- adding a new column in the table which will be the primary key. we will need this to safely update a table (without the use of where clause it we are not in safe mode to update a table)
ALTER TABLE transaction_summary
ADD transaction_id INT AUTO_INCREMENT,
ADD PRIMARY KEY (transaction_id);

select * from transaction_summary;
 

UPDATE transaction_summary
SET TOTAL_BALANCE = TOTAL_BALANCE + WITHDRAWAL_AMT - WITHDRAWAL_AMT
WHERE transaction_id IS NOT NULL;













