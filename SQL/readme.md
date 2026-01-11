# SQL
> SQL syntax can be written in either uppercase or lowercase letters.

## Commonly Used SQL Data Types

| Category  | Data Type          | Description                   | Size / Limit                                            | Example               |
| --------- | ------------------ | ----------------------------- | ------------------------------------------------------- | --------------------- |
| Numeric   | `INT`              | পূর্ণসংখ্যা সংরক্ষণ করে       | −2,147,483,648 to 2,147,483,647                         | `1`, `100`, `-20`     |
| Numeric   | `BIGINT`           | বড় আকারের পূর্ণসংখ্যা         | −9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 | `1234567890`          |
| Numeric   | `DECIMAL(p,s)`     | নির্ভুল দশমিক সংখ্যা          | Max precision: 65 digits (MySQL)                        | `DECIMAL(10,2)`       |
| Numeric   | `FLOAT`            | ভাসমান দশমিক সংখ্যা           | ~4 bytes (approx precision)                             | `12.34`               |
| Numeric   | `DOUBLE`           | বেশি প্রিসিশনের ভাসমান সংখ্যা | ~8 bytes (higher precision)                             | `123.4567`            |
| String    | `CHAR(n)`          | নির্দিষ্ট দৈর্ঘ্যের স্ট্রিং   | 0–255 characters                                        | `CHAR(10)`            |
| String    | `VARCHAR(n)`       | পরিবর্তনশীল দৈর্ঘ্যের স্ট্রিং | 0–65,535 characters (row size dependent)                | `VARCHAR(255)`        |
| String    | `TEXT`             | বড় টেক্সট সংরক্ষণ করে         | Max 65,535 characters                                   | Article, Description  |
| Date/Time | `DATE`             | শুধু তারিখ সংরক্ষণ করে        | `1000-01-01` to `9999-12-31`                            | `2026-01-11`          |
| Date/Time | `TIME`             | শুধু সময় সংরক্ষণ করে          | `-838:59:59` to `838:59:59`                             | `10:30:00`            |
| Date/Time | `DATETIME`         | তারিখ ও সময়                   | `1000-01-01 00:00:00` to `9999-12-31 23:59:59`          | `2026-01-11 10:30:00` |
| Date/Time | `TIMESTAMP`        | অটো টাইমস্ট্যাম্প             | `1970-01-01` to `2038-01-19` (MySQL)                    | Current time          |
| Boolean   | `BOOLEAN` / `BOOL` | সত্য বা মিথ্যা                | Internally stored as `TINYINT(1)`                       | `TRUE`, `FALSE`       |
| Others    | `ENUM`             | নির্দিষ্ট মানের তালিকা        | Max 65,535 values                                       | `'Male','Female'`     |
| Others    | `JSON`             | JSON ডেটা সংরক্ষণ করে         | Max 1GB (MySQL)                                         | `{ "id":1 }`          |

<br>

## Types of SQL Commands

| SQL Command Type | Full Form                    | Description (Bangla)                                                     | Common Commands                                      |
| ---------------- | ---------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------- |
| **DDL**          | Data Definition Language     | ডাটাবেস ও টেবিলের স্ট্রাকচার তৈরি, পরিবর্তন ও মুছে ফেলার জন্য ব্যবহৃত হয় | `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `RENAME`      |
| **DML**          | Data Manipulation Language   | টেবিলের ডেটা যোগ, পরিবর্তন ও মুছে ফেলার জন্য ব্যবহৃত হয়                  | `INSERT`, `UPDATE`, `DELETE`                         |
| **DQL**          | Data Query Language          | টেবিল থেকে ডেটা দেখার বা অনুসন্ধানের জন্য ব্যবহৃত হয়                     | `SELECT`                                             |
| **DCL**          | Data Control Language        | ইউজারের পারমিশন ও অ্যাক্সেস কন্ট্রোল করার জন্য ব্যবহৃত হয়                | `GRANT`, `REVOKE`                                    |
| **TCL**          | Transaction Control Language | ট্রানজ্যাকশন কন্ট্রোল ও ডেটা স্থায়ী করার জন্য ব্যবহৃত হয়                 | `COMMIT`, `ROLLBACK`, `SAVEPOINT`, `SET TRANSACTION` |

<br>

## Database Creation & Deletion Commands

```sql
CREATE DATABASE db_name;
DROP DATABASE db_name;

CREATE DATABASE IF NOT EXISTS db_name;
DROP DATABASE IF EXISTS db_name;
```

## View Databases
```sql
SHOW DATABASES;
```

## USE Command
> Before performing any operation on a table,  
> the relevant database must be selected.  
> This is done by executing the `USE db_name;` command.

<br>

# SQL General Order

```sql
```sql
SELECT      
DISTINCT     
FROM         
WHERE      
GROUP BY  
HAVING
ORDER BY     
LIMIT / OFFSET / TOP -- (ডাটাবেস ভেদে) 
```

<br>

# Table Related Queries

## Create Table
```sql
CREATE TABLE table_name(
  column_name1 datatype constraint,
  column_name1 datatype constraint,
  column_name1 datatype constraint
);

-- Do not put a comma after the last column.

CREATE TABLE student(
  student_id INT PRIMARY KEY,
  name VARCHAR(255),
  age INT NOT NULL
);
```

## View Tables
```sql
SHOW TABLES;
```

## View Table Data
```sql
SELECT * FROM table_name;
-- * Means all column
```

## Inser Data in Table
```sql
INSERT INTO table_name(column1, cloumn2)
VALUES (col1, col2), (col2, col3);


INSERT INTO student(student_id, name, age)
VALUES (3, 'col2', 18), (2, 'col3', 20);
```

## Defalt Value Constraint
> Sets the defalt value of a Column

```sql
CREATE TABLE student(
  student_id INT PRIMARY KEY,
  name VARCHAR(255),
  age INT DEFALT 25000
);
```

## Check Constraint
> it can limit the values allowed in a column
```sql
CREATE TABLE test(
  student_id INT PRIMARY KEY,
  name VARCHAR(255),
  age INT CHECK (age >= 18)
);

INSERT INTO test(student_id, name, age)
VALUES
(1, 'masud', 18);


-- ERROR
INSERT INTO test(student_id, name, age)
VALUES
(1, 'masud', 25);
```

## Update

> WHERE ক্লজ না দিলে পুরো টেবিলের সব রেকর্ড আপডেট হয়ে যাবে!

```sql
UPDATE table_name
SET col1 = val1, cal2 = val2
WHERE condition;

```

```sql
-- ১. পুরো একটা বিভাগের সব কর্মচারীর বেতন ১২% বাড়ানো
UPDATE employees
SET salary = salary * 1.12
WHERE department = 'Sales';


-- ২. ২০২৪ সালে জয়েন করা সবাইকে বোনাস দাও
UPDATE employees
SET bonus = 10000
WHERE hire_date >= '2024-01-01'
  AND hire_date <= '2024-12-31';


-- ৩. দাম ৫০০০+ এবং স্টক ১০ এর কম হলে স্টক আপডেট + স্ট্যাটাস চেঞ্জ
UPDATE products
SET 
    stock = stock + 50,
    status = 'low_stock_alert'
WHERE price > 5000 
  AND stock < 10;


-- ৪. একাধিক শর্ত দিয়ে অনেক রো আপডেট
UPDATE students
SET 
    status = 'passed',
    grade = 'A'
WHERE 
    marks >= 80 
    AND semester = 'Spring 2025'
    AND department IN ('CSE', 'EEE', 'ME');

-- সরাসরি employee_id জানো অনেক রো আপডেট
UPDATE employees
SET salary = salary + 10000
WHERE employee_id IN (103, 108);
```

## DELETE

- `DELETE` দিয়ে টেবিল থেকে এক বা একাধিক রেকর্ড (row) **স্থায়ীভাবে মুছে ফেলা** হয়।
- `WHERE` ক্লজ না দিলে পুরো টেবিলের সব রেকর্ড মুছে যাবে!

```sql
DELETE FROM table_name
WHERE condition;
```

```sql
-- ১. একজন নির্দিষ্ট কর্মচারীকে মুছে ফেলা
DELETE FROM employees
WHERE employee_id = 105;

-- ২. পুরো একটা বিভাগের সব কর্মচারী মুছে ফেলা
DELETE FROM employees
WHERE department = 'Intern';

-- ৩. একাধিক শর্ত দিয়ে মুছে ফেলা
DELETE FROM products
WHERE 
    category = 'Old Stock'
    AND stock = 0
    AND last_updated < '2024-01-01';
```




### Practice

```sql
CREATE TABLE IF NOT EXISTS employee(
  id INT PRIMARY KEY,
  name VARCHAR(255),
  salary INT
);

INSERT INTO employee(id, name, salary)
VALUES 
(1, 'adam', 2000),
(2, 'bob', 3000),
(3, 'masud', 25000);
```

<br>

# SELECT in Details
> used to select any data from the database

```sql

-- Select specific columns
SELECT col1, col2 FROM table_name;

-- Select all columns
SELECT * FROM table_name;

-- Select only unique values using DISTINCT


-- Select records with a condition (WHERE clause)
SELECT * FROM stu WHERE marks > 60;

```

<br>
# Limit Clause
> Limited row return

```sql
SELECT * FROM table_name LIMIT 3;

SELECT DISTINCT col1 FROM table_name LIMIT 2;

```

<br>

# Where Clause
> To Define some conditions


## SQL Operators (Used in WHERE Clause)
| Arithmetic Operators                               | Comparison Operators                                | Logical Operators                          | Bitwise Operators                            |                                          |
| -------------------------------------------------- | --------------------------------------------------- | ------------------------------------------ | -------------------------------------------- | ---------------------------------------- |
| `+` (Addition) <br> দুটি মান যোগ করে               | `=` (Equal) <br> দুই মান সমান কিনা যাচাই করে        | `AND` <br> সব শর্ত সত্য হলে true           | `&` (Bitwise AND) <br> bit-level AND অপারেশন |                                          |
| `-` (Subtraction) <br> দুটি মানের পার্থক্য বের করে | `!=` / `<>` (Not Equal) <br> সমান নয় কিনা যাচাই করে | `OR` <br> যেকোনো একটি শর্ত সত্য হলে true   | `                                            | ` (Bitwise OR) <br> bit-level OR অপারেশন |
| `*` (Multiplication) <br> দুটি মান গুণ করে         | `>` (Greater Than) <br> বড় কিনা যাচাই করে           | `NOT` <br> condition উল্টে দেয়             | `^` (Bitwise XOR) <br> bit-level XOR অপারেশন |                                          |
| `/` (Division) <br> ভাগ করে ফল দেয়                 | `<` (Less Than) <br> ছোট কিনা যাচাই করে             | `IN`, `NOT IN` <br> নির্দিষ্ট তালিকার মধ্যে আছে কিনা | `~` (Bitwise NOT) <br> bit invert করে        |                                          |
| `%` (Modulus) <br> ভাগশেষ বের করে                  | `>=` (Greater or Equal) <br> বড় বা সমান কিনা        | `BETWEEN` <br> নির্দিষ্ট range-এর মধ্যে    | `<<` (Left Shift) <br> bit বামে সরায়         |                                          |
|                                                    | `<=` (Less or Equal) <br> ছোট বা সমান কিনা          | `LIKE` <br> pattern অনুযায়ী মিল খোঁজে      | `>>` (Right Shift) <br> bit ডানে সরায়        |                                          |
|                                                    |                                                     | `IS NULL` <br> NULL মান আছে কিনা           |                                              |                                          |
|                                                    |                                                     | `IS NOT NULL` <br> NULL নয় কিনা            |                                              |                                          |

```sql
-- Select students with marks greater than 60
-- marks 60-এর বেশি হলে সেই সব রেকর্ড দেখায়
SELECT * FROM stu WHERE marks > 60;


-- Using arithmetic operation in WHERE clause
-- marks থেকে 10 বাদ দিয়ে যদি ফলাফল 60-এর বেশি হয়, সেই রেকর্ড দেখায়
SELECT * FROM stu WHERE marks - 10 > 60;


-- Using AND condition
-- marks 60-এর বেশি এবং city 'dilli' হলে সেই সব রেকর্ড দেখায়
SELECT * FROM stu WHERE marks > 60 AND city = 'dilli';


-- Using BETWEEN (range is inclusive)
-- marks 70 থেকে 90-এর মধ্যে হলে (inclusive) সেই সব রেকর্ড দেখায়
SELECT * FROM stu WHERE marks BETWEEN 70 AND 90;


-- Using IN (match any value from the list)
-- city যদি 'dilli' অথবা 'mumbai' হয়, সেই সব রেকর্ড দেখায়
SELECT * FROM stu WHERE city IN ('dilli', 'mumbai');


-- Using NOT IN (exclude specific values)
-- city যদি 'dilli' বা 'mumbai' না হয়, সেই সব রেকর্ড দেখায়
SELECT * FROM stu WHERE city NOT IN ('dilli', 'mumbai');
```

<br>
# Order By Clause
> To sort in ascending (ASC) or descending order (DESC)

```sql
SELECT * FROM table_name ORDER BY column_name ASC;


SELECT * FROM table_name ORDER BY column_name DESC; 

```

<br>

# ALTER TABLE
- `ALTER TABLE` দিয়ে ইতিমধ্যে তৈরি হয়ে যাওয়া টেবিলে পরিবর্তন করা হয়।

| কাজ                              | সিনট্যাক্স (সহজ উদাহরণ)                                                                 |
|----------------------------------|------------------------------------------------------------------------------------------|
| নতুন কলাম যোগ করা                | `ALTER TABLE employees ADD COLUMN bonus INT DEFAULT 0;`                                 |
| কলাম মুছে ফেলা                   | `ALTER TABLE employees DROP COLUMN bonus;`                                               |
| কলামের নাম পরিবর্তন               | `ALTER TABLE employees RENAME COLUMN old_name TO new_name;`                             |
| কলামের ডাটা টাইপ পরিবর্তন         | `ALTER TABLE employees ALTER COLUMN salary TYPE DECIMAL(12,2);`                         |
| NOT NULL যোগ করা                 | `ALTER TABLE employees ALTER COLUMN name SET NOT NULL;`                                  |
| NOT NULL মুছে ফেলা               | `ALTER TABLE employees ALTER COLUMN name DROP NOT NULL;`                                 |
| PRIMARY KEY যোগ করা              | `ALTER TABLE employees ADD PRIMARY KEY (employee_id);`                                   |
| FOREIGN KEY যোগ করা              | `ALTER TABLE employees ADD FOREIGN KEY (department_id) REFERENCES departments(department_id);` |
| UNIQUE CONSTRAINT যোগ করা        | `ALTER TABLE employees ADD UNIQUE (email);`                                              |
| DEFAULT ভ্যালু যোগ/পরিবর্তন      | `ALTER TABLE employees ALTER COLUMN status SET DEFAULT 'active';`                       |
| টেবিলের নাম পরিবর্তন             | `ALTER TABLE old_employees RENAME TO employees;`                                         |


```sql
-- ১. নতুন কলাম যোগ + ডিফল্ট ভ্যালু
ALTER TABLE employees
ADD COLUMN join_date DATE DEFAULT CURRENT_DATE;

-- ২. কলামের ডাটা টাইপ বড় করা (যদি ছোট থেকে বড় করতে চাও)
ALTER TABLE products
ALTER COLUMN description TYPE TEXT;

-- ৩. একসাথে একাধিক পরিবর্তন (PostgreSQL/MySQL)
ALTER TABLE employees
    ADD COLUMN phone VARCHAR(15),
    ALTER COLUMN salary TYPE DECIMAL(10,2),
    ALTER COLUMN salary SET DEFAULT 30000,
    DROP COLUMN temp_column;

-- ৪. FOREIGN KEY যোগ করা (পুরানো টেবিলে)
ALTER TABLE orders
ADD CONSTRAINT fk_customer
FOREIGN KEY (customer_id) 
REFERENCES customers(customer_id)
ON DELETE CASCADE;

-- ৫. ইনডেক্স যোগ করা (পারফরম্যান্সের জন্য)
ALTER TABLE employees
ADD INDEX idx_department (department_id);

```


<br>

<br>

---


# PK & FK

## Primary Key (PK) vs Foreign Key (FK)

| Feature          | Primary Key (PK)                               | Foreign Key (FK)                          |
| ---------------- | ---------------------------------------------- | ----------------------------------------- |
| Definition       | টেবিলের প্রতিটি রেকর্ডকে আলাদা করে চিহ্নিত করে | অন্য টেবিলের Primary Key-কে রেফার করে     |
| Uniqueness       | অবশ্যই ইউনিক হতে হবে                           | ইউনিক হওয়া বাধ্যতামূলক নয়                 |
| NULL Value       | NULL হতে পারে না                               | NULL হতে পারে                             |
| Number per Table | একটি টেবিলে মাত্র একটি Primary Key থাকে        | একটি টেবিলে একাধিক Foreign Key থাকতে পারে |
| Purpose          | টেবিলের প্রতিটি রোকে ইউনিকভাবে চিহ্নিত করা     | টেবিলগুলোর মধ্যে সম্পর্ক তৈরি করা         |
| Data Integrity   | Entity integrity নিশ্চিত করে                   | Referential integrity নিশ্চিত করে         |
| Index            | স্বয়ংক্রিয়ভাবে index তৈরি হয়                   | Index হতে পারে (DB অনুযায়ী)               |
| Duplicate Value  | গ্রহণযোগ্য নয়                                  | গ্রহণযোগ্য                                |
| Relation         | Parent table                                   | Child table                               |

## Primary Key (PK) Constraints
| Constraint Rule    | Description                                   |
| ------------------ | --------------------------------------------- |
| `UNIQUE`           | Primary Key-এর মান অবশ্যই ইউনিক হতে হবে       |
| `NOT NULL`         | Primary Key কখনো NULL হতে পারে না             |
| `ONE PER TABLE`    | একটি টেবিলে মাত্র একটি Primary Key থাকতে পারে |
| `AUTO INDEX`       | Primary Key স্বয়ংক্রিয়ভাবে index তৈরি করে     |
| `NO DUPLICATE`     | একই মান একাধিক রোতে থাকতে পারবে না            |
| `ENTITY INTEGRITY` | Entity integrity নিশ্চিত করে                  |


## Foreign Key (FK) Constraints

| Constraint Rule         | Description                                          |
| ----------------------- | ---------------------------------------------------- |
| `REFERENCES`            | অন্য টেবিলের Primary Key-কে রেফার করে                |
| `NULL ALLOWED`          | Foreign Key NULL হতে পারে                            |
| `MULTIPLE PER TABLE`    | একটি টেবিলে একাধিক Foreign Key থাকতে পারে            |
| `REFERENTIAL INTEGRITY` | টেবিলগুলোর মধ্যে সম্পর্ক বজায় রাখে                   |
| `ON DELETE`             | Parent row delete হলে child row-এর আচরণ নির্ধারণ করে |
| `ON UPDATE`             | Parent key update হলে child key-এর আচরণ নির্ধারণ করে |


## Common FK Actions

| Action               | Description                              |
| -------------------- | ---------------------------------------- |
| `ON DELETE CASCADE`  | Parent delete হলে child row-ও delete হবে |
| `ON DELETE SET NULL` | Parent delete হলে child key NULL হবে     |
| `ON DELETE RESTRICT` | Parent delete করা যাবে না                |
| `ON UPDATE CASCADE`  | Parent update হলে child update হবে       |

<br>

```sql
CREATE TABLE unique_test(
  id INT UNIQUE
);
INSERT INTO unique_test(id)
values(1);
-- The error is showing again because 1 has already been added.
INSERT INTO unique_test(id)
values(1);

-- Output: Duplicate Entry '1'
```

<br>
<br>

## Primary Key

---

```sql
CREATE TABLE city1(
  id INT,
  city_name VARCHAR(255),
  district_name VARCHAR(255),
  PRIMARY KEY (id)
);

CREATE TABLE city2(
  id INT PRIMARY KEY,
  city_name VARCHAR(255),
  district_name VARCHAR(255)
);

CREATE TABLE city3(
  id INT,
  city_name VARCHAR(255),
  district_name VARCHAR(255),
  PRIMARY KEY (id, city_name)
);
```



| Point          | city1       | city2        |
| -------------- | ----------- | ------------ |
| PK declaration | Table-level | Column-level |
| Behavior       | Same        | Same         |

### Table–3: city3 (Composite Primary Key)
>` id + city_name` মিলেই Primary Key
> এটাকে বলে `Composite Primary Key`

- `id` একা ইউনিক হওয়া জরুরি নয়
- `city_name` একাও ইউনিক হওয়া জরুরি নয়
- কিন্তু `id + city_name` একসাথে অবশ্যই ইউনিক হতে হব

| id | city_name  | Status    | Reason                                  |
| -- | ---------- | --------- | --------------------------------------- |
| 1  | Dhaka      | ✅ Valid   | Combination ইউনিক                       |
| 1  | Chittagong | ✅ Valid   | Combination ইউনিক                       |
| 2  | Dhaka      | ✅ Valid   | Combination ইউনিক                       |
| 1  | Dhaka      | ❌ Invalid | Duplicate `(id, city_name)` combination |




<br>

<br>

# SQL - FOREIGN KEY
**FOREIGN KEY** হলো একটা টেবিলের কলাম (বা কলামগুলো) যেটা অন্য আরেকটা টেবিলের **PRIMARY KEY** বা **UNIQUE** কলামের সাথে সম্পর্ক রাখে।  
এটা ডাটাবেসে **রেফারেন্সিয়াল ইন্টিগ্রিটি** (referential integrity) বজায় রাখে।

1. **departments** টেবিল (বিভাগ)  
   - department_id (PK)  
   - department_name  

2. **employees** টেবিল (কর্মচারী)  
   - employee_id (PK)  
   - name  
   - department_id ← এটাই FOREIGN KEY (যেটা departments টেবিলের department_id কে রেফার করে)
  
```sql
CREATE TABLE departments (
    department_id   INT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);

CREATE TABLE employees (
    employee_id     INT PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    department_id   INT,
    
    FOREIGN KEY (department_id) 
        REFERENCES departments(department_id)
);
```

### আলাদা করে FOREIGN KEY যোগ করা (পরে)

```sql
ALTER TABLE employees
ADD FOREIGN KEY (department_id) 
REFERENCES departments(department_id);
```

### সবচেয়ে বেশি ব্যবহৃত উদাহরণ (CASCADE)

```sql
CREATE TABLE employees (
    employee_id     INT PRIMARY KEY,
    name            VARCHAR(100),
    department_id   INT,
    
    FOREIGN KEY (department_id) 
        REFERENCES departments(department_id)
        ON DELETE CASCADE           -- বিভাগ ডিলিট হলে সব কর্মচারীও অটো ডিলিট
        ON UPDATE CASCADE           -- বিভাগের আইডি চেঞ্জ হলে কর্মচারীর আইডিও চেঞ্জ
);
```


<br>

# Aggregate Function

| Function  | Description                     |
| --------- | ------------------------------- |
| `COUNT()` | মোট রেকর্ডের সংখ্যা গণনা করে    |
| `SUM()`   | নির্দিষ্ট কলামের সব মান যোগ করে |
| `AVG()`   | নির্দিষ্ট কলামের গড় মান বের করে |
| `MIN()`   | সবচেয়ে ছোট মান বের করে          |
| `MAX()`   | সবচেয়ে বড় মান বের করে           |

```sql
-- Count total students
-- মোট কতজন ছাত্র আছে তা দেখায়
SELECT COUNT(*) FROM stu;

-- Calculate total marks
-- সব ছাত্রের marks যোগ করে মোট মান দেখায়
SELECT SUM(marks) FROM stu;

-- Calculate average marks
-- সব ছাত্রের marks-এর গড় মান দেখায়
SELECT AVG(marks) FROM stu;

-- Find minimum marks
-- সবচেয়ে কম marks কত তা দেখায়
SELECT MIN(marks)
FROM stu;

-- Find maximum marks
-- সবচেয়ে বেশি marks কত তা দেখায়
SELECT MAX(marks) FROM stu;

-- Calculate average marks excluding specific cities
-- city যদি 'dilli' বা 'mumbai' না হয়, সেই সব ছাত্রের marks-এর গড় দেখায়
SELECT AVG(marks) FROM stu WHERE city NOT IN ('dilli', 'mumbai');
```

<br>

# GROUP BY clause
> GROUP BY একই কলামের মান অনুযায়ী রেকর্ডগুলোকে গ্রুপ করে  
> এবং প্রতিটি গ্রুপের উপর aggregate function প্রয়োগ করতে সাহায্য করে।  
> Generally we use group by with some aggregate function

- `SELECT` এ যে কলামগুলো **অ্যাগ্রিগেট ফাংশনের** ভিতরে নেই, সেগুলো অবশ্যই `GROUP BY` এ লিখতে হবে।
- `GROUP BY` সাধারণত `WHERE` এর পরে এবং `ORDER BY` এর আগে লেখা হয়।


## Basic Syntax
```sql
```sql
SELECT 
    column1,
    column2,
    AGGREGATE_FUNCTION(column3)
FROM 
    table_name
WHERE 
    condition
GROUP BY 
    column1, column2
ORDER BY 
    column1;
```
```sql
SELECT city, name FROM stu GROUP BY city, name;
| city   | name    |
| ------ | ------- |
| dilli  | anil    |
| Mumbai | Bhumika |
| mumbai | chaya   |
| rajos  | anil    |
| dilli  | ema     |
| dilli  | farhan  |

SELECT city, MAX(marks) FROM stu GROUP BY city;
| city   | MAX(marks) |
| ------ | ---------- |
| dilli  | 78         |
| Mumbai | 93         |
| rajos  | 50         |

```

## Common Mistake
```
-- ভুল (এটা চলবে না বা ভুল রেজাল্ট দেবে)
SELECT 
    department,
    name,           -- ← এটা GROUP BY এ নেই এবং অ্যাগ্রিগেটও নেই
    SUM(salary)
FROM employees GROUP BY department;

-- সঠিক উপায় 

-- ১. সব নন-অ্যাগ্রিগেট কলাম GROUP BY তে আনা
SELECT department, name, SUM(salary)
FROM employees
GROUP BY department, name;

-- ২. অথবা শুধু যেটা দরকার সেটাই নেওয়া
SELECT department, SUM(salary)
FROM employees
GROUP BY department;
```

<br>

```sql
SELECT city, COUNT(*) FROM stu GROUP BY city;
```
- `COUNT(*)` → counts total students in each city
- Includes all rows for that city



<br>

# Having Clause 
> Similar to Where
> Applies some condition on rows

`HAVING` ক্লজ ব্যবহার করা হয় **গ্রুপ করা ডাটার উপর শর্ত** দেওয়ার জন্য।  
এটা মূলত `WHERE` এর মতোই কাজ করে, কিন্তু পার্থক্য হলো:

| বিষয়               | WHERE                              | HAVING                                   |
|---------------------|------------------------------------|------------------------------------------|
| কখন কাজ করে        | রো (row) ফিল্টার করে GROUP BY এর আগে | গ্রুপ করার পরে অ্যাগ্রিগেটের উপর ফিল্টার |
| কোন কলামে কাজ করে   | টেবিলের আসল কলামগুলোতে             | অ্যাগ্রিগেট ফাংশনের রেজাল্টে (SUM, COUNT ইত্যাদি) |
| GROUP BY এর সাথে    | থাকতে পারে বা না থাকতে পারে        | সাধারণত GROUP BY এর সাথেই ব্যবহার হয়    |


```sql
SELECT 
    column1,
    AGGREGATE_FUNCTION(column2)
FROM 
    table_name
WHERE 
    normal_condition
GROUP BY 
    column1
HAVING 
    AGGREGATE_FUNCTION(column2) condition
ORDER BY 
    column1;


SELECT city, marks FROM stu GROUP BY city, marks HAVING MAX(marks) > 90;
```

```sql
-- ১. যে বিভাগে ১০ জনের বেশি কর্মচারী আছে
SELECT 
    department,
    COUNT(*) AS employee_count
FROM 
    employees
GROUP BY 
    department
HAVING 
    COUNT(*) > 10;

-- ২. যে বিভাগের গড় বেতন ৮০,০০০+ টাকা
SELECT 
    department,
    ROUND(AVG(salary), 2) AS avg_salary
FROM 
    employees
GROUP BY 
    department
HAVING 
    AVG(salary) >= 80000
ORDER BY 
    avg_salary DESC;

-- ৩. যে বিভাগে মোট বেতন ৫০ লাখের বেশি এবং কমপক্ষে ৫ জন কর্মচারী
SELECT 
    department,
    COUNT(*) AS total_employees,
    SUM(salary) AS total_salary
FROM 
    employees
GROUP BY 
    department
HAVING 
    COUNT(*) >= 5 
    AND SUM(salary) > 5000000
ORDER BY 
    total_salary DESC;
```

## Common Mistake

```sql
-- ভুল (এটা চলবে না)
SELECT department, AVG(salary)
FROM employees
WHERE AVG(salary) > 50000          -- ← WHERE এ অ্যাগ্রিগেট ব্যবহার করা যায় না!
GROUP BY department;

-- সঠিক উপায়
SELECT department, AVG(salary)
FROM employees
GROUP BY department
HAVING AVG(salary) > 50000;
```



<br>

# ALIAS
- ALIAS মানে **অন্য নাম দেওয়া**।

```sql
SELECT 
    employee_id AS id,              -- employee_id কে id বলে ডাকা হলো
    first_name || ' ' || last_name AS full_name,  -- এক্সপ্রেশনের ALIAS
    salary * 12 AS annual_salary
FROM employees;



SELECT 
    e.name, 
    d.department_name
FROM employees AS e          -- employees টেবিলকে e বলে ডাকা
JOIN departments AS d        -- departments কে d বলা
    ON e.department_id = d.department_id;
```


# JOIN

| JOIN টাইপ | অর্থ (সহজ ভাষায়) | কখন ব্যবহার করবো? | সিনট্যাক্স উদাহরণ |
|----------|------------------|-------------------|------------------|
| INNER JOIN | শুধু দুই টেবিলের মধ্যে যেগুলো **মিলে যায়** সেই রো দেখাবে | সাধারণ ক্ষেত্রে, সবচেয়ে বেশি ব্যবহার হয় | `INNER JOIN` |
| LEFT JOIN / LEFT OUTER JOIN | বাম টেবিলের সব রো + ডান টেবিলের মিলে যাওয়া রো (না মিললে `NULL`) | যখন বাম টেবিলের সব ডাটা চাই | `LEFT JOIN` |
| RIGHT JOIN / RIGHT OUTER JOIN | ডান টেবিলের সব রো + বাম টেবিলের মিলে যাওয়া রো | যখন ডান টেবিলের সব ডাটা চাই | `RIGHT JOIN` |
| FULL OUTER JOIN | দুই টেবিলের সব রো (মিলে যাওয়া + না মিলে যাওয়া সব) | যখন দুই দিকেরই সব ডাটা চাই | `FULL OUTER JOIN` |
| CROSS JOIN | প্রত্যেক রো সবার সাথে মিলবে (Cartesian Product) | খুব কম ব্যবহার হয়, সাধারণত টেস্টিংয়ে | `CROSS JOIN` |


```sql
-- ১. INNER JOIN (সবচেয়ে কমন)
SELECT 
    e.employee_id,
    e.name AS employee_name,
    d.department_name,
    e.salary
FROM employees e
INNER JOIN departments d
    ON e.department_id = d.department_id
WHERE e.salary > 50000
ORDER BY e.salary DESC;

-- ২. LEFT JOIN (সব কর্মচারী দেখাবে, বিভাগ না থাকলেও)
SELECT 
    e.name,
    e.salary,
    d.department_name
FROM employees e
LEFT JOIN departments d
    ON e.department_id = d.department_id;

-- ৩. একই টেবিলে JOIN (self-join) - ম্যানেজারের নাম দেখা
SELECT 
    e.employee_id,
    e.name AS employee,
    m.name AS manager
FROM employees e
LEFT JOIN employees m
    ON e.manager_id = m.employee_id;

-- ৪. তিনটা টেবিল JOIN
SELECT 
    e.name,
    d.department_name,
    l.city
FROM employees e
INNER JOIN departments d ON e.department_id = d.department_id
INNER JOIN locations l ON d.location_id = l.location_id;
```

<br>

**employees** টেবিল (বাম দিকে)

| employee_id | name       | dept_id |

|-------------|------------|---------|

| 1           | Rahim      | 101     |

| 2           | Karim      | 102     |

| 3           | Sumon      | 103     |

| 4           | Rina       | NULL    |



**departments** টেবিল (ডান দিকে)

| dept_id | dept_name     |

|---------|---------------|

| 101     | Sales         |

| 102     | Marketing     |

| 104     | HR            |


### 1. INNER JOIN 

শুধু যেগুলো দুই টেবিলেই মিলে গেছে সেগুলোই দেখাবে।  

```sql

SELECT e.name, d.dept_name

FROM employees e

INNER JOIN departments d ON e.dept_id = d.dept_id;

```

**ফলাফল:**

| name   | dept_name   |

|--------|-------------|

| Rahim  | Sales       |

| Karim  | Marketing   |

→ Sumon আর Rina দেখা যায়নি কারণ তাদের dept_id departments টেবিলে নেই।  
