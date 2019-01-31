INSERT INTO Companies(ID, NAME, URL ) VALUES(1, 'TestCorp', 'example.com');
INSERT INTO Users(ID, CompanyID, Firstname, Surname, AccessLevel, Email, Password, StripeID, Verified, SubID) VALUES (1, 1, 'John', 'Smith', 'Owner', 'test@test.test', '?', 'cus_D3qdko6i2SfRLE', 'True', 'sub_DL4V736hIisRHk');
INSERT INTO UserSettings(ID, CompanyID, AdminPermissions, UserPermissions ) VALUES(1, 1, 'EditChatbots:True;EditUsers:True;AccessBilling:False;', 'EditChatbots:True;EditUsers:False;AccessBilling:False;');
INSERT INTO Databases(ID, CompanyID, Message, Nickname) VALUES (1, 1, 'Hello, I am a test assistant! Nice to meet you.', 'Test Assistant');
INSERT INTO Products(ID, AssistantID, ProductID, Name, Brand, Model, Price, Keywords, Discount, URL) VALUES(1, 1, 'L512', 'House', 'Newport', 'Refurbished', '£500', 'house,refurbished,1bedroom', '0%', 'example.com');

INSERT INTO Questions(ID, AssistantID, Question, Type) VALUES(1, 1, 'Question 1', 'userInfoRetrieval');
INSERT INTO Questions(ID, AssistantID, Question, Type) VALUES(2, 1, 'Question 2', 'dbRetrieval');
INSERT INTO Questions(ID, AssistantID, Question, Type) VALUES(3, 1, 'Question 3', 'userInfoRetrieval');

INSERT INTO Answers(ID, QuestionID, Answer, Keyword) VALUES(1, 2, 'Answer 1', 'house');

INSERT INTO Plans(ID, Nickname) VALUES('plan_D3lpeLZ3EV8IfA', 'ultimate');
INSERT INTO Plans(ID, Nickname) VALUES('plan_D3lp9R7ombKmSO', 'advanced');
INSERT INTO Plans(ID, Nickname) VALUES('plan_D3lp2yVtTotk2f', 'basic');
INSERT INTO Plans(ID, Nickname) VALUES('plan_D48N4wxwAWEMOH', 'debug');