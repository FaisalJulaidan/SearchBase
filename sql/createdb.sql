DROP TABLE IF EXISTS Companies;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Assistants;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Statistics;
DROP TABLE IF EXISTS Questions;
DROP TABLE IF EXISTS Answers;
DROP TABLE IF EXISTS UserInput;
DROP TABLE IF EXISTS Plans;


CREATE TABLE 'Companies' (
	'ID'	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	'Name'	TEXT NOT NULL,
	'Size'	TEXT,
	'URL'	TEXT NOT NULL,
	'PhoneNumber' TEXT
);

CREATE TABLE 'Users' (
	'ID'	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	'CompanyID'	INTEGER NOT NULL,
	'Firstname'	TEXT NOT NULL,
	'Surname'	TEXT NOT NULL,
	'AccessLevel'	TEXT NOT NULL,
	'Email'	TEXT NOT NULL UNIQUE,
	'Password'	BLOB NOT NULL,
  'StripeID'	TEXT UNIQUE DEFAULT NULL,
	'Verified'	TEXT DEFAULT 'False',

	FOREIGN KEY('CompanyID') REFERENCES 'Companies'('ID')
);

CREATE TABLE 'Assistants' (
	'ID'	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	'CompanyID'	INTEGER NOT NULL,
	'Route'	TEXT UNIQUE,
	'Message'	TEXT NOT NULL,
	'SecondsUntilPopup'	TEXT NOT NULL DEFAULT 'Off',
	'Nickname' TEXT NOT NULL UNIQUE,
	'Active' TEXT NOT NULL DEFAULT 'True'
);

CREATE TABLE 'Products' (
	'ID'	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	'AssistantID'	INTEGER NOT NULL,
	'ProductID'	INTEGER NOT NULL,
	'Name'	TEXT NOT NULL,
	'Brand'	TEXT NOT NULL,
	'Model'	TEXT NOT NULL,
	'Price'	TEXT NOT NULL,
	'Keywords'	TEXT NOT NULL,
	'Discount'	TEXT NOT NULL,
	'URL'	TEXT NOT NULL,
	FOREIGN KEY('AssistantID') REFERENCES 'Assistants'('ID')
);

CREATE TABLE 'Statistics' (
	'ID'	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	'AssistantID'	INTEGER NOT NULL,
	'Date'	TEXT NOT NULL,
	'Opened'	INTEGER NOT NULL DEFAULT 0,
	'QuestionsAnswered'	INTEGER NOT NULL DEFAULT 0,
	'ProductsReturned'	INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE 'Questions' (
	'ID'	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	'AssistantID'	INTEGER NOT NULL,
	'Question'	TEXT NOT NULL,
	'Type'	TEXT NOT NULL,
	FOREIGN KEY('AssistantID') REFERENCES 'Assistants'('ID')
);

CREATE TABLE 'Answers' (
	'ID'	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	'QuestionID'	INTEGER NOT NULL,
	'Answer'	TEXT NOT NULL,
	'Keyword'	TEXT NOT NULL,
	'TimesClicked' INTEGER NOT NULL DEFAULT 0,
	'Action' TEXT NOT NULL DEFAULT 'Next Question by Order'
);

CREATE TABLE 'UserInput' (
	'ID'	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	'QuestionID'	INTEGER NOT NULL,
	'Date'	TEXT NOT NULL,
	'Input'	TEXT NOT NULL
);

CREATE TABLE 'Plans' (
	'ID'	TEXT NOT NULL PRIMARY KEY UNIQUE,
	'Nickname'	TEXT NOT NULL UNIQUE
);