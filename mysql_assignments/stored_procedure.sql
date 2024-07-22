show databases;
use practical;
show tables;

select * from employee;


-- starting the stored procedure
DELIMITER //

CREATE PROCEDURE SelectAllEmployee()
BEGIN
    SELECT * FROM Employee;
END //

DELIMITER ;


CALL SelectAllEmployee();


-- Creating a Stored Procedure with an Input Parameter
DELIMITER //

CREATE PROCEDURE getEmployeeBySalary(IN salaryfilter INT )
--  The IN keyword tells the database that the parameter will be passed by the calling
--  salaryfilter is an arbitrary name for the parameter.
--  int  is the datatype. it is the datatype for command after where statement below
 
BEGIN
    SELECT * FROM Employee where salary > salaryfilter;
END //

DELIMITER ;

CALL getEmployeeBySalary(444638);

