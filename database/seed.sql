--Shelter
INSERT INTO Shelter (Shelter_ID, Name, Location, Contact) VALUES
(1, 'Taipei Happy Dog Home', '台北市大安區', '02-27001234'),
(2, 'Taichung Paws Shelter', '台中市西屯區', '04-23005678'),
(3, 'Kaohsiung Love Center', '高雄市左營區', '07-31009012');

--Users
INSERT INTO Users (User_ID, Role, Email, Password_Hash) VALUES
(1, 1, 'admin1@test.com', 'hash_admin1'),
(2, 1, 'staff1@test.com', 'hash_staff1'),
(3, 1, 'staff2@test.com', 'hash_staff2'),
(4, 0, 'user1@test.com', 'hash_user1'),
(5, 0, 'user2@test.com', 'hash_user2'),
(6, 0, 'user3@test.com', 'hash_user3'),
(7, 0, 'user4@test.com', 'hash_user4'),
(8, 0, 'user5@test.com', 'hash_user5'),
(9, 0, 'user6@test.com', 'hash_user6'),
(10, 0, 'user7@test.com', 'hash_user7');


--Dog
INSERT INTO Dog (Dog_ID, Shelter_ID, Name, Gender, Age, Breed, Image_URL, AI_Story) VALUES
     (1, 1, 'Alex', 'Male', 11, 'Boxer', NULL, NULL),
     (2, 1, 'Rachel', 'Female', 13.25, 'Rhodesian Ridgeback Mix', NULL, NULL),
     (3, 1, 'Vacok', 'Male', 2.42, 'Dachshund, Fox Terrier Mix', NULL, NULL),
     (4, 1, 'Borzas', 'Male', 10.75, 'Tibetan Terrier', NULL, NULL),
     (5, 1, 'Alma', 'Female', 12.92, 'Unknown Mix', NULL, NULL),
     (6, 1, 'Perec', 'Male', 8.08, 'Unknown Mix', NULL, NULL),
     (7, 1, 'Buddy', 'Male', 6.08, 'Unknown Mix', NULL, NULL),
     (8, 1, 'Max', 'Male', 7.5, 'Golden Retriever', NULL, NULL),
     (9, 1, 'Dani', 'Male', 10.08, 'Staffordshire Terrier Mix', NULL, NULL),
     (10, 1, 'Pepe', 'Male', 6.83, 'Dachshund Mix', NULL, NULL),
     (11, 2, 'Coco', 'Female', 5.75, 'Dachshund Mix', NULL, NULL),
     (12, 2, 'Limo', 'Female', 8.5, 'Unknown Mix', NULL, NULL),
     (13, 2, 'Benga', 'Male', 6.75, 'Unknown Mix', NULL, NULL),
     (14, 2, 'Brico', 'Male', 6.75, 'Unknown Mix', NULL, NULL),
     (15, 2, 'Bond', 'Male', 6.75, 'Unknown Mix', NULL, NULL),
     (16, 2, 'Brikett', 'Male', 8.17, 'Schnauzer Mix', NULL, NULL),
     (17, 2, 'Blikk', 'Male', 6.5, 'Bernese Mountain Dog Mix', NULL, NULL),
     (18, 2, 'Nugat', 'Male', 7.42, 'German Pointer Mix', NULL, NULL),
     (19, 2, 'Kanga', 'Female', 6.33, 'Schnauzer Mix', NULL, NULL),
     (20, 2, 'Szergely', 'Male', 7, 'Unknown Mix', NULL, NULL),
     (21, 3, 'Kiskutya', 'Female', 6.58, 'Unknown Mix', NULL, NULL),
     (22, 3, 'Keverek', 'Female', 6.08, 'Unknown Mix', NULL, NULL),
     (23, 3, 'Maci', 'Male', 16.17, 'Unknown Mix', NULL, NULL),
     (24, 3, 'Lucky', 'Male', 7.25, 'Unknown Mix', NULL, NULL),
     (25, 3, 'Toto', 'Male', 7.17, 'Siberian Husky Mix', NULL, NULL),
     (26, 3, 'Lili', 'Female', 7.08, 'Unknown Mix', NULL, NULL),
     (27, 3, 'Spicc', 'Male', 11.58, 'Spitz', NULL, NULL),
     (28, 3, 'Missy', 'Female', 7, 'Unknown Mix', NULL, NULL),
     (29, 3, 'Rozsdi', 'Male', 14.42, 'Unknown Mix', NULL, NULL),
     (30, 3, 'Rudy', 'Male', 9.33, 'Staffordshire Terrier Mix', NULL, NULL),
     (31, 1, 'Szormok', 'Male', 14.92, 'Unknown Mix', NULL, NULL),
     (32, 1, 'Tundi', 'Female', 8.25, 'Unknown Mix', NULL, NULL),
     (33, 1, 'Szemi', 'Female', 7.25, 'Unknown Mix', NULL, NULL),
     (34, 1, 'Kendy', 'Male', 7.08, 'Unknown Mix', NULL, NULL),
     (35, 1, 'Elhagyott', 'Female', 8.25, 'Unknown Mix', NULL, NULL),
     (36, 2, 'Drive', 'Female', 9.5, 'Unknown Mix', NULL, NULL),
     (37, 2, 'Gina', 'Female', 12.58, 'Unknown Mix', NULL, NULL),
     (38, 2, 'Maci2', 'Male', 7.83, 'Unknown Mix', NULL, NULL),
     (39, 2, 'Roxi', 'Female', 7.92, 'Rottweiler Mix', NULL, NULL),
     (40, 2, 'Bator', 'Male', 8, 'Unknown Mix', NULL, NULL);

-- User_Shelter
INSERT INTO User_Shelter (User_ID, Shelter_ID) VALUES (1, 1), (2, 2), (3, 3);

-- Application
INSERT INTO Application (App_ID, User_ID, Dog_ID, Status, Match_Score) VALUES
(1, 6, 1, 0, 88), -- User 6 申請 Alex (待審)
(2, 7, 2, 1, 95), -- User 7 申請 Rachel (已核准)
(3, 8, 3, 2, 45), -- User 8 申請 Vacok (被拒絕)
(4, 9, 8, 0, 72), -- User 9 申請 Max (待審)
(5, 10, 11, 1, 80); -- User 10 申請 Coco (已核准)

-- Health_record
INSERT INTO Health_record (Record_ID, Dog_ID, Administered_Date, Vaccine_Name) VALUES
(1, 1, '2023-01-10', '狂犬病疫苗'),
(2, 1, '2023-06-15', '核心疫苗'),
(3, 2, '2023-03-20', '狂犬病疫苗'),
(4, 8, '2023-09-01', '心絲蟲預防'),
(5, 11, '2023-11-05', '核心疫苗');