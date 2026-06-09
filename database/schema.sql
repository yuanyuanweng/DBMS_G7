-- 1. 建立 Shelter (收容所)
CREATE TABLE Shelter (
    Shelter_ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Location TEXT NOT NULL,
    Contact TEXT
);

-- 2. 建立 Users (使用者)
CREATE TABLE Users (
    User_ID INTEGER PRIMARY KEY,
    Role INTEGER NOT NULL CHECK (Role IN (0, 1)), -- 0:領養人, 1: 動物收容所工作人員（可以新增狗狗、管理 shelter、審核 application）
    Email TEXT NOT NULL UNIQUE,
    Password_Hash TEXT NOT NULL
);

-- 3. 建立 Dog (狗狗)
CREATE TABLE Dog (
    Dog_ID INTEGER PRIMARY KEY,
    Shelter_ID INTEGER NOT NULL,
    Name TEXT NOT NULL,
    Gender TEXT CHECK (Gender IN ('Male', 'Female', 'Unknown')),
    Age INTEGER CHECK (Age >= 0),
    Breed TEXT,
    Image_URL TEXT,
    Description TEXT,
    FOREIGN KEY (Shelter_ID) REFERENCES Shelter(Shelter_ID)
);

-- 4. 建立 Application (申請單)
CREATE TABLE Application (
    App_ID INTEGER PRIMARY KEY,
    User_ID INTEGER NOT NULL,
    Dog_ID INTEGER NOT NULL,
    Status INTEGER NOT NULL DEFAULT 0 CHECK (Status IN (0, 1, 2)), -- 0:待審(pending), 1:核准(approved), 2:拒絕(rejected) (管理員層面)
    Match_Score INTEGER CHECK (Match_Score BETWEEN 0 AND 100),
    Created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    Full_Name TEXT,
    Phone TEXT,
    City TEXT,
    Housing_Type TEXT,
    Reason TEXT,
    Lifestyle TEXT,
    UNIQUE(User_ID, Dog_ID),
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Dog_ID) REFERENCES Dog(Dog_ID)
);

-- 5. 建立 Health_record (健康紀錄)
CREATE TABLE Health_record (
    Record_ID INTEGER PRIMARY KEY,
    Dog_ID INTEGER NOT NULL,
    Administered_Date DATE NOT NULL,
    Vaccine_Name TEXT NOT NULL,
    FOREIGN KEY (Dog_ID) REFERENCES Dog(Dog_ID)
);

-- 6. 建立 User_Shelter
CREATE TABLE User_Shelter (
    User_ID INTEGER NOT NULL,
    Shelter_ID INTEGER NOT NULL,
    PRIMARY KEY (User_ID, Shelter_ID),
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Shelter_ID) REFERENCES Shelter(Shelter_ID)
);

-- Dog Status (狗狗的領養狀態)
DROP VIEW IF EXISTS Dog_With_Status;
CREATE VIEW Dog_With_Status AS
SELECT 
    d.Dog_ID,
    d.Shelter_ID,
    d.Name,
    d.Gender,
    d.Age,
    d.Breed,
    d.Image_URL,
    d.Description,
    CASE
        WHEN COUNT(CASE WHEN a.Status = 1 THEN 1 END) > 0 THEN 'Adopted'
        WHEN COUNT(CASE WHEN a.Status = 0 THEN 1 END) > 0 THEN 'Pending'
        ELSE 'Available'
    END AS Availability
FROM Dog d
LEFT JOIN Application a 
    ON d.Dog_ID = a.Dog_ID
GROUP BY d.Dog_ID;
