-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: sp
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `academic_calender`
--

DROP TABLE IF EXISTS `academic_calender`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `academic_calender` (
  `Activity` varchar(70) NOT NULL,
  `Date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `academic_calender`
--

LOCK TABLES `academic_calender` WRITE;
/*!40000 ALTER TABLE `academic_calender` DISABLE KEYS */;
INSERT INTO `academic_calender` VALUES ('Academic registration 2nd Year B.Tech & 2nd Year (B.Sc., BCA)','2026-07-15'),('Class work begins (2nd, 3rd and 4th Years)','2026-07-16'),('Independence Day ','2026-08-15'),('Fresher?s Day# ','2026-09-11'),('Midterm Exam','2026-09-18'),('Mahatma Gandhi Jayanthi ','2026-10-02'),('Last day of instruction (2nd, 3rd and 4th Years) ','2026-11-13'),('Comprehensive Exam Begins (2nd, 3rd and 4th Years) ','2026-11-16'),('Comprehensive Exam Ends (2nd, 3rd and 4th Years) ','2026-12-04'),('Winter Break Begins','2026-12-19'),('Winter Break Ends','2026-12-31');
/*!40000 ALTER TABLE `academic_calender` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendence`
--

DROP TABLE IF EXISTS `attendence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendence` (
  `Enroll_No` varchar(20) NOT NULL,
  `Name` text NOT NULL,
  `Course` text NOT NULL,
  `Section` varchar(10) NOT NULL,
  `Session` varchar(10) NOT NULL,
  `Date` date NOT NULL,
  `Status` enum('Present','Absent') DEFAULT NULL,
  `year` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendence`
--

LOCK TABLES `attendence` WRITE;
/*!40000 ALTER TABLE `attendence` DISABLE KEYS */;
INSERT INTO `attendence` VALUES ('24STCHH010122','Rahul','AIDS','E','2','2026-09-01','Absent',3),('24STUCHH010156','Veena','AIDS','E','2','2026-09-01','Present',3),('24STUCHH010163','Aman','AIDS','E','2','2026-09-01','Present',3),('24STCHH010171','Reena','AIDS','E','2','2026-09-01','Present',3),('24STCHH010172','Kumar','AIDS','E','2','2026-09-01','Present',3),('24STCHH010187','Jagan','AIDS','E','2','2026-09-01','Absent',3),('24STCHH010190','Meena','AIDS','E','2','2026-09-01','Absent',3),('24STCHH010192','Akansha','AIDS','E','2','2026-09-01','Present',3),('24STCHH010198','Arun','AIDS','E','2','2026-09-01','Present',3),('24STCHH010211','Balu','AIDS','E','2','2026-09-01','Present',3),('24STCHH010215','Bhagya','AIDS','E','2','2026-09-01','Present',3),('24STCHH010217','Sharan','AIDS','E','2','2026-09-01','Present',3),('24STCHH010225','Sreenidhi','AIDS','E','2','2026-09-01','Present',3),('24STCHH010250','Ayaan','AIML','H','4','2026-09-01',NULL,3),('24STCHH010252','Mark','AIML','H','4','2026-09-01',NULL,3),('24STCHH010259','Lasya','AIML','H','4','2026-09-01',NULL,3),('24STCHH010265','Keshav','AIML','H','4','2026-09-01',NULL,3),('24STCHH010299','Mathew','AIML','H','4','2026-09-01',NULL,3),('24STCHH010310','Omar','AIML','H','4','2026-09-01',NULL,3),('24STCHH010315','Manjula','AIML','H','4','2026-09-01',NULL,3),('24STCHH010316','Megha','AIML','H','4','2026-09-01',NULL,3),('24STCHH010320','Bose','AIML','H','4','2026-09-01',NULL,3),('24STCHH010322','Rishi','AIML','H','4','2026-09-01','Absent',3),('24STCHH010329','Riksheta','AIML','H','4','2026-09-01',NULL,3),('24STCHH010122','Rahul','AIDS','E','3','2026-09-02',NULL,3),('24STUCHH010156','Veena','AIDS','E','3','2026-09-02',NULL,3),('24STUCHH010163','Aman','AIDS','E','3','2026-09-02',NULL,3),('24STCHH010171','Reena','AIDS','E','3','2026-09-02',NULL,3),('24STCHH010172','Kumar','AIDS','E','3','2026-09-02',NULL,3),('24STCHH010187','Jagan','AIDS','E','3','2026-09-02',NULL,3),('24STCHH010190','Meena','AIDS','E','3','2026-09-02',NULL,3),('24STCHH010192','Akansha','AIDS','E','3','2026-09-02',NULL,3),('24STCHH010198','Arun','AIDS','E','3','2026-09-02',NULL,3),('24STCHH010211','Balu','AIDS','E','3','2026-09-02',NULL,3),('24STCHH010215','Bhagya','AIDS','E','3','2026-09-02',NULL,3),('24STCHH010217','Sharan','AIDS','E','3','2026-09-02',NULL,3),('24STCHH010225','Sreenidhi','AIDS','E','3','2026-09-02',NULL,3),('24STCHH010250','Ayaan','AIML','H','6','2026-09-02',NULL,3),('24STCHH010252','Mark','AIML','H','6','2026-09-02',NULL,3),('24STCHH010259','Lasya','AIML','H','6','2026-09-02',NULL,3),('24STCHH010265','Keshav','AIML','H','6','2026-09-02',NULL,3),('24STCHH010299','Mathew','AIML','H','6','2026-09-02',NULL,3),('24STCHH010310','Omar','AIML','H','6','2026-09-02',NULL,3),('24STCHH010315','Manjula','AIML','H','6','2026-09-02',NULL,3),('24STCHH010316','Megha','AIML','H','6','2026-09-02',NULL,3),('24STCHH010320','Bose','AIML','H','6','2026-09-02',NULL,3),('24STCHH010322','Rishi','AIML','H','6','2026-09-02',NULL,3),('24STCHH010329','Riksheta','AIML','H','6','2026-09-02',NULL,3);
/*!40000 ALTER TABLE `attendence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timetable`
--

DROP TABLE IF EXISTS `timetable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timetable` (
  `Day` varchar(11) NOT NULL,
  `9:30 - 10:20` text NOT NULL,
  `10:20 - 11:10` varchar(50) NOT NULL,
  `11:25 - 12:15` varchar(50) NOT NULL,
  `12:15 - 1:05` varchar(50) NOT NULL,
  `1:45 - 2:35` varchar(50) NOT NULL,
  `2:35 - 3:20` varchar(50) NOT NULL,
  `3:20 - 4:15` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timetable`
--

LOCK TABLES `timetable` WRITE;
/*!40000 ALTER TABLE `timetable` DISABLE KEYS */;
INSERT INTO `timetable` VALUES ('Monday','BT| Section: III(E)| Room:113','DBMS| Section: II(A)| Room:110','BT| Section:III(B)| Room:212',' ','DBMS(Lab)| Section: II(E)| Room:VLSA','DBMS(Lab)| Section: II(E)| Room:VLSA','BT| Section: III(B)| Room:220'),('Tuesday','DBMS| Section: II(E)| Room:204','DBMS| Section: II(D)| Room:G04','BT| Section:III(C)| Room:G06','BT| Section: II(C)| Room:111 ',' ','DBMS| Section: II(A)| Room:101','BT| Section: III(E)| Room:212'),('Wednesday',' ','BT| Section: III(D)| Room:G05','BT| Section:III(E)| Room:G08','DBMS| Section: II(F)| Room:110 ','BT| Section:III(B)| Room:221 ','DBMS(Lab)| Section: II(E)| Room:111','DBMS(Lab)| Section: II(E)| Room:111'),('Thursday',' ','DBMS| Section: II(A)| Room:G07','BT| Section:III(E)| Room:G03','BT| Section: III(C)| Room:110','BT| Section:III(D)| Room:109','DBMS| Section: II(A)| Room:101','DBMS| Section: II(B)| Room:121'),('Friday','DBMS(Lab)| Section: II(C)| Room:222','DBMS(Lab)| Section: II(C)| Room:222','BT| Section:III(A)| Room:G02',' ','BT| Section:III(A)| Room:211','DBMS| Section: II(C)| Room:108',' ');
/*!40000 ALTER TABLE `timetable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('vasudev','scrypt:32768:8:1$ysnU0J3sRy6eVGm3$aa96c45e4df0ed1f09809ee791e22b0b7b3c1b5ae6e64f79f3b040fe607980f53025bb7b363cbdcfd97ea16e4d57d04fc4a2f4c3337621206492ede16c61ba6a'),('vasuudev','scrypt:32768:8:1$pYL4VwqRZuLs12EL$f5bb714d9df96e36c84bc9709a93cbd218ad1857852f81604bd220bba9a3b85299131f0dde98a96ac1ce27345cec3991c36c81c3df4d06e8023c8f5ecaf03ad9'),('zaheer','scrypt:32768:8:1$EMkOh7tFtQSx3ORl$e350338842cfd1bdc8a533b6fa148b15e46e2d9c6b7587a772c72bdafd186db855f3281a35e9fc56eb7bb68f8ef52646546149bdc54ff8e97fb80f042a2b8121');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-12 18:40:20
