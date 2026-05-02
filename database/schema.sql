-- 1. 建立 Shelter (收容所)
CREATE TABLE Shelter (
    Shelter_ID INTEGER PRIMARY KEY,
    Name TEXT,
    Location TEXT,
    Contact TEXT
);

-- 2. 建立 Users (使用者)
CREATE TABLE Users (
    User_ID INTEGER PRIMARY KEY,
    Role INTEGER CHECK (Role IN (0, 1)), -- 0:領養人, 1:志工
    Email TEXT,
    Password_Hash TEXT
);

-- 3. 建立 Dog (狗狗)
CREATE TABLE Dog (
    Dog_ID INTEGER PRIMARY KEY,
    Shelter_ID INTEGER,
    Name TEXT,
    Gender TEXT,
    Age INTEGER,
    Breed TEXT,
    Image_URL TEXT,
    AI_Story TEXT,
    FOREIGN KEY (Shelter_ID) REFERENCES Shelter(Shelter_ID)
);

-- 4. 建立 Application (申請單)
CREATE TABLE Application (
    App_ID INTEGER PRIMARY KEY,
    User_ID INTEGER,
    Dog_ID INTEGER,
    Status INTEGER CHECK (Status IN (0, 1, 2)), -- 0:待審, 1:核准, 2:拒絕
    Match_Score INTEGER,
    Created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Dog_ID) REFERENCES Dog(Dog_ID)
);

-- 5. 建立 Health_record (健康紀錄)
CREATE TABLE Health_record (
    Record_ID INTEGER PRIMARY KEY,
    Dog_ID INTEGER,
    Administered_Date DATE,
    Vaccine_Name TEXT,
    FOREIGN KEY (Dog_ID) REFERENCES Dog(Dog_ID)
);

-- 6. 建立 User_Shelter
CREATE TABLE User_Shelter (
    User_ID INTEGER,
    Shelter_ID INTEGER,
    PRIMARY KEY (User_ID, Shelter_ID),
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Shelter_ID) REFERENCES Shelter(Shelter_ID)
);