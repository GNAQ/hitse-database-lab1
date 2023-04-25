CREATE TABLE student(
	Sid char(8) NOT NULL,
	Sname char(18) NOT NULL,
	Ssex char(4), 
	Sage integer, 
	SClass char(6),
	PRIMARY KEY(Sid),
);

CREATE TABLE course(
	Cid char(4) NOT NULL,
	Cname char(30) NOT NULL, 
	Credit float(1),
	Chours integer,
	Tid char(3),
	PRIMARY KEY(Cid)
);

CREATE TABLE score(
	Sid char(8) NOT NULL,
	Cid char(4) NOT NULL,
	Score float(1),
	FOREIGN KEY(Sid) REFERENCES student(Sid),
	FOREIGN KEY(Cid) REFERENCES course(Cid)
);

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\course.csv'
INTO TABLE course
FIELDS TERMINATED BY ','