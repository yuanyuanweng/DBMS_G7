--Shelter
INSERT INTO Shelter (Shelter_ID, Name, Location, Contact) VALUES
(1, 'Taipei Happy Dog Home', '台北市大安區', '02-27001234'),
(2, 'Taichung Paws Shelter', '台中市西屯區', '04-23005678'),
(3, 'Kaohsiung Love Center', '高雄市左營區', '07-31009012');

--Users
INSERT INTO Users (User_ID, Role, Email, Password_Hash) VALUES
(1, 1, 'admin1@test.com', 'scrypt:32768:8:1$smzLOMoDV1h3KX4E$2edc365c1427dc773c55f37790cf4961a03df22cb815b69c4f129a96e23cc60602ff6fe16bc727ba9fca40b9dae4558d76b55598411ce3a7223daf5890d94e7d'), --admin1
(2, 1, 'staff1@test.com', 'scrypt:32768:8:1$fONXM3VZT8xbbvK5$4b9f82dd17ff99352468895dd2c2e58e7c4e274c116f2591f32bcabb192fbaf2dec74e422c2b729bffbac585d9bd6df8d07b1922ce61dce607a8836be20c77c7'), --staff1
(3, 1, 'staff2@test.com', 'scrypt:32768:8:1$QleAAyr9W26IsFZE$7d2b3b62e50206ec95f6dc8d271f7c1acfe4e44a0e9ca08cc2749c43ef460f540250c6f6126d0a73edf629f3214ae32b00cc946d0a8822cdf6636c680c3daff1'), --staff2
(4, 0, 'user1@test.com', 'scrypt:32768:8:1$eXwZaZjOEtzmOYGo$09d35c7eca9917ffe1080f72f23bb4efdd7c6e66faf3201955e73ee6279682919b20dac12560525de0031ffa9853bf12ed156f971031bad96d88e2d58ab53f26'), --user1
(5, 0, 'user2@test.com', 'scrypt:32768:8:1$MVx8RS8TTALrkqb3$af48e4d0fccaadda6a64cd825944b561fdb88e86fb743a51c3567201101b93fc98bb6c051926604687172806344ac1d61f9482ad504a4e6dd8abffce9822452c'), --user2
(6, 0, 'user3@test.com', 'scrypt:32768:8:1$GPLMGLXAgbky9wza$ffdd264682d063776436f54625455d80aff1afbab2e3a9e825d9fb8250adda9fafa9a7a8fd21400746b75c709b6564da0b4f048c9b59593e7ee41d779453ac4e'), --user3
(7, 0, 'user4@test.com', 'scrypt:32768:8:1$cR9EruPGlX3LU9SH$ecf6f4486fc19c6dbb82eb623ed6feaab98d6afb91a1a6fb929ee1631c20d6deaaeb9661d5a7c7ba9f017924f0c4419c8cad9b06a333e7995cd210815afc7861'), --user4
(8, 0, 'user5@test.com', 'scrypt:32768:8:1$YOA3k2Ehy1gczcIC$a96d2f19a37a15465b8adeb4847ff1337bed9b61e6ffc8da6c4c4147bc322eb3d2137e848734d9f4762af1d51609e44394509bbd863b640d87bf93510386a166'), --user5
(9, 0, 'user6@test.com', 'scrypt:32768:8:1$M6WEfTNzWCTB6NEO$7680f4d589d397714225ef572206dac9a557e070dad9aed35ad971d0f3fca14e0298535467005f6ec125506647c0d66af09507edb109d30fb300274ad8cf5a18'), --user6
(10, 0, 'user7@test.com', 'scrypt:32768:8:1$ePQOwYOrwzOctxAT$130194e7b62c1384cc120ed054fb36aec7d0a454fc02c05e8a8cff741f962403c14b9e88c483b790a1eb5ec788bd290f94803dd6011058d4477b6fe03c18acd8'); --user7

-- Dog
INSERT INTO Dog (Dog_ID, Shelter_ID, Name, Gender, Age, Breed, Image_URL) VALUES
     (1, 1, 'Alex', 'Male', 11, 'Boxer', NULL),
     (2, 1, 'Rachel', 'Female', 13, 'Rhodesian Ridgeback Mix', NULL),
     (3, 1, 'Vacok', 'Male', 2, 'Dachshund, Fox Terrier Mix', NULL),
     (4, 1, 'Borzas', 'Male', 10, 'Tibetan Terrier', NULL),
     (5, 1, 'Alma', 'Female', 12, 'Unknown Mix', NULL),
     (6, 1, 'Perec', 'Male', 8, 'Unknown Mix', NULL),
     (7, 1, 'Buddy', 'Male', 6, 'Unknown Mix', NULL),
     (8, 1, 'Max', 'Male', 7, 'Golden Retriever', NULL),
     (9, 1, 'Dani', 'Male', 10, 'Staffordshire Terrier Mix', NULL),
     (10, 1, 'Pepe', 'Male', 6, 'Dachshund Mix', NULL),
     (11, 2, 'Coco', 'Female', 5, 'Dachshund Mix', NULL),
     (12, 2, 'Limo', 'Female', 8, 'Unknown Mix', NULL),
     (13, 2, 'Benga', 'Male', 6, 'Unknown Mix', NULL),
     (14, 2, 'Brico', 'Male', 6, 'Unknown Mix', NULL),
     (15, 2, 'Bond', 'Male', 6, 'Unknown Mix', NULL),
     (16, 2, 'Brikett', 'Male', 8, 'Schnauzer Mix', NULL),
     (17, 2, 'Blikk', 'Male', 6, 'Bernese Mountain Dog Mix', NULL),
     (18, 2, 'Nugat', 'Male', 7, 'German Pointer Mix', NULL),
     (19, 2, 'Kanga', 'Female', 6, 'Schnauzer Mix', NULL),
     (20, 2, 'Szergely', 'Male', 7, 'Unknown Mix', NULL),
     (21, 3, 'Kiskutya', 'Female', 6, 'Unknown Mix', NULL),
     (22, 3, 'Keverek', 'Female', 6, 'Unknown Mix', NULL),
     (23, 3, 'Maci', 'Male', 16, 'Unknown Mix', NULL),
     (24, 3, 'Lucky', 'Male', 7, 'Unknown Mix', NULL),
     (25, 3, 'Toto', 'Male', 7, 'Siberian Husky Mix', NULL),
     (26, 3, 'Lili', 'Female', 7, 'Unknown Mix', NULL),
     (27, 3, 'Spicc', 'Male', 11, 'Spitz', NULL),
     (28, 3, 'Missy', 'Female', 7, 'Unknown Mix', NULL),
     (29, 3, 'Rozsdi', 'Male', 14, 'Unknown Mix', NULL),
     (30, 3, 'Rudy', 'Male', 9, 'Staffordshire Terrier Mix', NULL),
     (31, 1, 'Szormok', 'Male', 14, 'Unknown Mix', NULL),
     (32, 1, 'Tundi', 'Female', 8, 'Unknown Mix', NULL),
     (33, 1, 'Szemi', 'Female', 7, 'Unknown Mix', NULL),
     (34, 1, 'Kendy', 'Male', 7, 'Unknown Mix', NULL),
     (35, 1, 'Elhagyott', 'Female', 8, 'Unknown Mix', NULL),
     (36, 2, 'Drive', 'Female', 9, 'Unknown Mix', NULL),
     (37, 2, 'Gina', 'Female', 12, 'Unknown Mix', NULL),
     (38, 2, 'Maci2', 'Male', 7, 'Unknown Mix', NULL),
     (39, 2, 'Roxi', 'Female', 7, 'Rottweiler Mix', NULL),
     (40, 2, 'Bator', 'Male', 8, 'Unknown Mix', NULL);

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