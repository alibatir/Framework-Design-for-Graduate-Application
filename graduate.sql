-- MySQL dump 10.13  Distrib 8.0.24, for Win64 (x86_64)
--
-- Host: localhost    Database: graduate
-- ------------------------------------------------------
-- Server version	8.0.24

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
-- Table structure for table `GRADE_CLUSTER`
--

DROP TABLE IF EXISTS `GRADE_CLUSTER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `GRADE_CLUSTER` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `GRADE` varchar(45) DEFAULT NULL,
  `MAX_GPA` double DEFAULT NULL,
  `MIN_GPA` double DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `GRADE_CLUSTER`
--

LOCK TABLES `GRADE_CLUSTER` WRITE;
/*!40000 ALTER TABLE `GRADE_CLUSTER` DISABLE KEYS */;
INSERT INTO `GRADE_CLUSTER` VALUES (1,'A*',0,0),(2,'A',4,3.5),(3,'B',0,0),(4,'C',3.4,2.5),(5,'D',0,0);
/*!40000 ALTER TABLE `GRADE_CLUSTER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `KEYWORD`
--

DROP TABLE IF EXISTS `KEYWORD`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `KEYWORD` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `KEYWORD` varchar(45) DEFAULT NULL,
  `university_id` int DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `KEYWORD`
--

LOCK TABLES `KEYWORD` WRITE;
/*!40000 ALTER TABLE `KEYWORD` DISABLE KEYS */;
/*!40000 ALTER TABLE `KEYWORD` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `REQUIREMENTS`
--

DROP TABLE IF EXISTS `REQUIREMENTS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `REQUIREMENTS` (
  `ID` int NOT NULL,
  `ALES_MIN` double DEFAULT NULL,
  `GRE_MIN` double DEFAULT NULL,
  `YDS_MIN` double DEFAULT NULL,
  `IELTS_OVERALL_MIN` double DEFAULT NULL,
  `IELTS_WRITE_MIN` double DEFAULT NULL,
  `TOEFL_OVERALL_MIN` double DEFAULT NULL,
  `TOEFL_WRITE_MIN` double DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Graduate Applications REQUIREMENTS';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `REQUIREMENTS`
--

LOCK TABLES `REQUIREMENTS` WRITE;
/*!40000 ALTER TABLE `REQUIREMENTS` DISABLE KEYS */;
INSERT INTO `REQUIREMENTS` VALUES (1,85,165,55,6.5,6.5,79,22);
/*!40000 ALTER TABLE `REQUIREMENTS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UNIVERSITY`
--

DROP TABLE IF EXISTS `UNIVERSITY`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `UNIVERSITY` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `NAME` varchar(45) DEFAULT NULL,
  `CLUSTER` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UNIVERSITY`
--

LOCK TABLES `UNIVERSITY` WRITE;
/*!40000 ALTER TABLE `UNIVERSITY` DISABLE KEYS */;
/*!40000 ALTER TABLE `UNIVERSITY` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-02 23:41:08
