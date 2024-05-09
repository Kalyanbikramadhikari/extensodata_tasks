show databases;
use practical;
select * from employee;


select Emp_Name from employee where Emp_No = 1;

create INDEX emp_index ON employee(Emp_No, Emp_Name(20), Dept(20), Salary, Date_Join, Location(30), email_id(20), Age);
select * from employee;

select * from employee where Emp_No = '10';
SHOW INDEX FROM employee;



