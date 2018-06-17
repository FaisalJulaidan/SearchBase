INSERT INTO Companies(ID, NAME, URL, Subscription, StripeID) VALUES(1, 'TestCorp', 'example.com', 'Debug', 'cus_D3qdko6i2SfRLE');
INSERT INTO Users(ID, CompanyID, Firstname, Surname, AccessLevel, Email, Password, Verified) VALUES (1, 1, 'John', 'Smith', 'Admin', 'test@test.test', '', 'True');
INSERT INTO Assistants(ID, CompanyID, Message) VALUES (1, 1, 'Hello, I am a test assistant! Nice to meet you.');
INSERT INTO Products(ID, AssistantID, ProductID, Name, Brand, Model, Price, Keywords, Discount, URL) VALUES(1, 1, 'L512', 'House', 'Newport', 'Refurbished', '£500', 'house,refurbished,1bedroom', '0%', 'example.com');

INSERT INTO Questions(ID, AssistantID, Question, Type) VALUES(1, 1, 'Question 1', 'userInfoRetrieval');
INSERT INTO Questions(ID, AssistantID, Question, Type) VALUES(2, 1, 'Question 2', 'dbRetrieval');
INSERT INTO Questions(ID, AssistantID, Question, Type) VALUES(3, 1, 'Question 3', 'userInfoRetrieval');

INSERT INTO Answers(ID, QuestionID, Answer, Keyword) VALUES(1, 2, 'Answer 1', 'house');