CREATE DATABASE  IF NOT EXISTS `collabspace` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `collabspace`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: collabspace
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
-- Table structure for table `accounts_profile`
--

DROP TABLE IF EXISTS `accounts_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_profile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bio` longtext COLLATE utf8mb4_unicode_ci,
  `avatar_url` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  `role` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `project_links` longtext COLLATE utf8mb4_unicode_ci,
  `avatar_file` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_profile_user_id_49a85d32_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_profile`
--

LOCK TABLES `accounts_profile` WRITE;
/*!40000 ALTER TABLE `accounts_profile` DISABLE KEYS */;
INSERT INTO `accounts_profile` VALUES (1,'резонирует....','http://127.0.0.1:8000/media/profiles/avatars/6ca31378ce92860018a47b20c46460f5.jpg','2025-12-12 04:07:27.731086','2025-12-25 09:16:49.291939',1,'author',1,'','profiles/avatars/6ca31378ce92860018a47b20c46460f5.jpg'),(2,'скучно...','http://127.0.0.1:8000/media/profiles/avatars/2f45a5cb19dbf5bc9dc82d34df83b786.jpg','2025-12-25 00:24:27.500018','2025-12-25 01:06:53.799011',2,'user',0,NULL,'profiles/avatars/2f45a5cb19dbf5bc9dc82d34df83b786.jpg'),(3,NULL,NULL,'2025-12-25 02:17:23.559145','2025-12-25 02:17:23.559145',3,'user',0,NULL,'');
/*!40000 ALTER TABLE `accounts_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'admin');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,1,5),(6,1,6),(7,1,7),(8,1,8),(9,1,9),(10,1,10),(11,1,11),(12,1,12),(13,1,13),(14,1,14),(15,1,15),(16,1,16),(17,1,17),(18,1,18),(19,1,19),(20,1,20),(21,1,21),(22,1,22),(23,1,23),(24,1,24),(25,1,25),(26,1,26),(27,1,27),(28,1,28);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add profile',7,'add_profile'),(26,'Can change profile',7,'change_profile'),(27,'Can delete profile',7,'delete_profile'),(28,'Can view profile',7,'view_profile'),(29,'Can add Проект',8,'add_project'),(30,'Can change Проект',8,'change_project'),(31,'Can delete Проект',8,'delete_project'),(32,'Can view Проект',8,'view_project'),(33,'Can add Участник проекта',9,'add_projectparticipant'),(34,'Can change Участник проекта',9,'change_projectparticipant'),(35,'Can delete Участник проекта',9,'delete_projectparticipant'),(36,'Can view Участник проекта',9,'view_projectparticipant'),(37,'Can add Понравившийся проект',10,'add_projectfavorite'),(38,'Can change Понравившийся проект',10,'change_projectfavorite'),(39,'Can delete Понравившийся проект',10,'delete_projectfavorite'),(40,'Can view Понравившийся проект',10,'view_projectfavorite'),(41,'Can add Приглашение в проект',11,'add_projectinvitation'),(42,'Can change Приглашение в проект',11,'change_projectinvitation'),(43,'Can delete Приглашение в проект',11,'delete_projectinvitation'),(44,'Can view Приглашение в проект',11,'view_projectinvitation'),(45,'Can add Задача',12,'add_task'),(46,'Can change Задача',12,'change_task'),(47,'Can delete Задача',12,'delete_task'),(48,'Can view Задача',12,'view_task'),(49,'Can add Комментарий',13,'add_comment'),(50,'Can change Комментарий',13,'change_comment'),(51,'Can delete Комментарий',13,'delete_comment'),(52,'Can view Комментарий',13,'view_comment'),(53,'Can add Уведомление',14,'add_notification'),(54,'Can change Уведомление',14,'change_notification'),(55,'Can delete Уведомление',14,'delete_notification'),(56,'Can view Уведомление',14,'view_notification');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1200000$NFtdjlo4yLn98DAHhP8S8A$rX4kScUOu171tmADu1Wz7eJN4H6g+aAxYc/+iCveJkw=','2025-12-25 13:54:12.613966',1,'admin','','','',1,1,'2025-12-11 11:20:36.000000'),(2,'pbkdf2_sha256$1200000$aaKz0hRONTkHbiwC5BQ4Of$QaPrZr59xCl3Og602MZjzDqAUZRygUA+gLGTVq21vHQ=','2025-12-25 00:24:27.505924',0,'wrx666','','','',0,1,'2025-12-25 00:24:26.508262'),(3,'pbkdf2_sha256$1200000$YbT30QGgTtZhB7QG28Dxtm$UMQ0h3uh4CQQA/TTiPgdITgs6XQL0hFHRQZ1yZf8BiA=','2025-12-25 02:17:23.573519',0,'wrx6661','','','',0,1,'2025-12-25 02:17:22.240296');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
INSERT INTO `auth_user_user_permissions` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,1,5),(6,1,6),(7,1,7),(8,1,8),(9,1,9),(10,1,10),(11,1,11),(12,1,12),(13,1,13),(14,1,14),(15,1,15),(16,1,16),(17,1,17),(18,1,18),(19,1,19),(20,1,20),(21,1,21),(22,1,22),(23,1,23),(24,1,24),(25,1,25),(26,1,26),(27,1,27),(28,1,28);
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-12-12 04:42:07.297280','1','admin',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(2,'2025-12-12 04:44:51.486601','1','admin',1,'[{\"added\": {}}]',2,1),(3,'2025-12-12 04:45:03.646795','1','Профиль admin',2,'[{\"changed\": {\"fields\": [\"\\u0420\\u043e\\u043b\\u044c\"]}}]',7,1),(4,'2025-12-12 07:09:21.054221','1','Профиль admin',2,'[{\"changed\": {\"fields\": [\"\\u0412\\u0435\\u0440\\u0438\\u0444\\u0438\\u0446\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\"]}}]',7,1),(5,'2025-12-12 07:09:37.119804','1','Профиль admin',2,'[{\"changed\": {\"fields\": [\"\\u0412\\u0435\\u0440\\u0438\\u0444\\u0438\\u0446\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\"]}}]',7,1),(6,'2025-12-24 23:28:44.588181','1','Профиль admin',2,'[{\"changed\": {\"fields\": [\"\\u0420\\u043e\\u043b\\u044c\"]}}]',7,1),(7,'2025-12-25 09:09:24.310958','1','Профиль admin',2,'[{\"changed\": {\"fields\": [\"\\u0412\\u0435\\u0440\\u0438\\u0444\\u0438\\u0446\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\"]}}]',7,1),(8,'2025-12-25 09:12:15.151093','1','Профиль admin',2,'[{\"changed\": {\"fields\": [\"\\u0412\\u0435\\u0440\\u0438\\u0444\\u0438\\u0446\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\"]}}]',7,1),(9,'2025-12-25 09:13:00.666193','1','Профиль admin',2,'[{\"changed\": {\"fields\": [\"\\u0412\\u0435\\u0440\\u0438\\u0444\\u0438\\u0446\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\"]}}]',7,1),(10,'2025-12-25 09:15:58.023245','1','Профиль admin',2,'[{\"changed\": {\"fields\": [\"\\u0412\\u0435\\u0440\\u0438\\u0444\\u0438\\u0446\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\"]}}]',7,1),(11,'2025-12-25 09:16:49.292936','1','Профиль admin',2,'[{\"changed\": {\"fields\": [\"\\u0412\\u0435\\u0440\\u0438\\u0444\\u0438\\u0446\\u0438\\u0440\\u043e\\u0432\\u0430\\u043d\"]}}]',7,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (7,'accounts','profile'),(1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(13,'projects','comment'),(14,'projects','notification'),(8,'projects','project'),(10,'projects','projectfavorite'),(11,'projects','projectinvitation'),(9,'projects','projectparticipant'),(12,'projects','task'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-12-11 11:20:00.966554'),(2,'auth','0001_initial','2025-12-11 11:20:01.587885'),(3,'admin','0001_initial','2025-12-11 11:20:01.731895'),(4,'admin','0002_logentry_remove_auto_add','2025-12-11 11:20:01.748990'),(5,'admin','0003_logentry_add_action_flag_choices','2025-12-11 11:20:01.755971'),(6,'contenttypes','0002_remove_content_type_name','2025-12-11 11:20:01.878794'),(7,'auth','0002_alter_permission_name_max_length','2025-12-11 11:20:01.946570'),(8,'auth','0003_alter_user_email_max_length','2025-12-11 11:20:01.967107'),(9,'auth','0004_alter_user_username_opts','2025-12-11 11:20:01.975089'),(10,'auth','0005_alter_user_last_login_null','2025-12-11 11:20:02.039464'),(11,'auth','0006_require_contenttypes_0002','2025-12-11 11:20:02.041459'),(12,'auth','0007_alter_validators_add_error_messages','2025-12-11 11:20:02.050436'),(13,'auth','0008_alter_user_username_max_length','2025-12-11 11:20:02.118307'),(14,'auth','0009_alter_user_last_name_max_length','2025-12-11 11:20:02.187212'),(15,'auth','0010_alter_group_name_max_length','2025-12-11 11:20:02.204507'),(16,'auth','0011_update_proxy_permissions','2025-12-11 11:20:02.213474'),(17,'auth','0012_alter_user_first_name_max_length','2025-12-11 11:20:02.281622'),(18,'sessions','0001_initial','2025-12-11 11:20:02.320402'),(19,'accounts','0001_initial','2025-12-12 04:07:10.187963'),(20,'accounts','0002_profile_project_link_profile_role_profile_verified','2025-12-12 04:39:38.330354'),(21,'accounts','0003_remove_profile_project_link_profile_project_links','2025-12-12 04:43:48.188226'),(22,'projects','0001_initial','2025-12-24 23:42:52.349227'),(23,'accounts','0004_profile_avatar_file_alter_profile_avatar_url','2025-12-24 23:57:38.536990'),(24,'projects','0002_projectparticipant','2025-12-25 00:18:22.141249'),(25,'projects','0003_projectfavorite','2025-12-25 01:13:41.458852'),(26,'projects','0004_projectinvitation','2025-12-25 01:32:21.396469'),(27,'projects','0005_task','2025-12-25 02:12:01.504832'),(28,'projects','0006_comment','2025-12-25 02:19:49.730531'),(29,'projects','0007_notification','2025-12-25 09:58:38.639377');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('0an0tpmwss573f2khwbrj8nafqqqpjiu','.eJxVjDsKwzAQRO-iOoiVvV5ByvQ5g1h9NnISJLDsyuTukcFFAlO9eTO7cryt2W0tLW6O6qqMuvwyz-GVylHEJ5dH1aGWdZm9PhR9tk3fa0zv2-n-HWRuua-tMRaFUrQ9QuOAAcAjjcZ4CIySLDB1MAWSCUlAIqAHoYGNhaQ-X9onN7o:1vTwPG:MsQuOeVlfsE7dwjhXQZI3w9-N17qOX_tGxKrD-sJXfQ','2025-12-26 06:13:34.974329'),('0epeo9lbjl8cg079oi68v5mvaebsrjea','.eJxVjDsKwzAQRO-iOoiVvV5ByvQ5g1h9NnISJLDsyuTukcFFAlO9eTO7cryt2W0tLW6O6qqMuvwyz-GVylHEJ5dH1aGWdZm9PhR9tk3fa0zv2-n-HWRuua-tMRaFUrQ9QuOAAcAjjcZ4CIySLDB1MAWSCUlAIqAHoYGNhaQ-X9onN7o:1vYkBA:GYTqU2TF0TQGtCTpWM1v_avgTR977tQbP1QPQnkQAJU','2026-01-08 12:10:52.436576'),('pk6x9upviqhz7orkzspj2l3t7swmeog2','.eJxVjDsKwzAQRO-iOoiVvV5ByvQ5g1h9NnISJLDsyuTukcFFAlO9eTO7cryt2W0tLW6O6qqMuvwyz-GVylHEJ5dH1aGWdZm9PhR9tk3fa0zv2-n-HWRuua-tMRaFUrQ9QuOAAcAjjcZ4CIySLDB1MAWSCUlAIqAHoYGNhaQ-X9onN7o:1vYkdI:XdMp9XnM22bmLngRczvLUHCJ4MR3zeZattxlfFBU9MI','2026-01-08 12:39:56.599228'),('t30e781xh5cg33g3kv7lxnn40c3jkg4m','.eJxVjDsKwzAQRO-iOoiVvV5ByvQ5g1h9NnISJLDsyuTukcFFAlO9eTO7cryt2W0tLW6O6qqMuvwyz-GVylHEJ5dH1aGWdZm9PhR9tk3fa0zv2-n-HWRuua-tMRaFUrQ9QuOAAcAjjcZ4CIySLDB1MAWSCUlAIqAHoYGNhaQ-X9onN7o:1vYlnA:oYcbZ8-5V6vpOnur0QsCfzU47KcuJjH3ZmJS270Masg','2026-01-08 13:54:12.620818'),('yfxdhqvuui737locp771xok86bvvk0hr','.eJxVjDsOwjAQBe_iGln2ZtfBlPScwVr_cADZUpxUiLuTSCmgfTPz3sLxuhS39jS7KYqLAHH63TyHZ6o7iA-u9yZDq8s8ebkr8qBd3lpMr-vh_h0U7mWryWRIAQ1pMozKIngeh0F5S0CAkLLVAfMwZoWUY9CMOViLSqvzVkTx-QK-MTcN:1vYZ9X:sBm5H0e-mNycSyMOLqXeL1AzgVz916XCK3_ptwb5RGQ','2026-01-08 00:24:27.508320');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects_comment`
--

DROP TABLE IF EXISTS `projects_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects_comment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `text` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `author_id` int NOT NULL,
  `parent_id` bigint DEFAULT NULL,
  `project_id` bigint DEFAULT NULL,
  `task_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `projects_comment_author_id_eec213f3_fk_auth_user_id` (`author_id`),
  KEY `projects_comment_parent_id_a3fb47d3_fk_projects_comment_id` (`parent_id`),
  KEY `projects_comment_project_id_220d4b34_fk_projects_project_id` (`project_id`),
  KEY `projects_comment_task_id_37596e2f_fk_projects_task_id` (`task_id`),
  CONSTRAINT `projects_comment_author_id_eec213f3_fk_auth_user_id` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `projects_comment_parent_id_a3fb47d3_fk_projects_comment_id` FOREIGN KEY (`parent_id`) REFERENCES `projects_comment` (`id`),
  CONSTRAINT `projects_comment_project_id_220d4b34_fk_projects_project_id` FOREIGN KEY (`project_id`) REFERENCES `projects_project` (`id`),
  CONSTRAINT `projects_comment_task_id_37596e2f_fk_projects_task_id` FOREIGN KEY (`task_id`) REFERENCES `projects_task` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects_comment`
--

LOCK TABLES `projects_comment` WRITE;
/*!40000 ALTER TABLE `projects_comment` DISABLE KEYS */;
INSERT INTO `projects_comment` VALUES (1,'123','2025-12-25 09:30:15.351315','2025-12-25 09:30:15.352311',1,NULL,8,NULL),(2,'123','2025-12-25 09:38:02.685515','2025-12-25 09:38:02.685515',1,1,8,NULL),(3,'123','2025-12-25 09:50:20.751798','2025-12-25 09:50:20.751798',2,NULL,NULL,2),(4,'123','2025-12-25 09:59:07.758910','2025-12-25 09:59:07.758910',1,NULL,8,NULL),(5,'123','2025-12-25 09:59:22.249945','2025-12-25 09:59:22.249945',2,NULL,8,NULL),(6,'123','2025-12-25 10:04:27.231998','2025-12-25 10:04:27.231998',1,5,8,NULL),(7,'123','2025-12-25 10:05:00.928829','2025-12-25 10:05:00.928829',2,NULL,8,NULL),(8,'123','2025-12-25 10:05:11.794992','2025-12-25 10:05:11.794992',1,7,8,NULL),(9,'123','2025-12-25 10:06:48.943297','2025-12-25 10:06:48.943297',2,NULL,8,NULL),(10,'123','2025-12-25 10:06:57.438494','2025-12-25 10:06:57.439491',1,9,8,NULL),(11,'123','2025-12-25 12:41:01.347538','2025-12-25 12:41:01.347538',2,NULL,1,NULL),(12,'123','2025-12-25 12:41:11.696065','2025-12-25 12:41:11.696065',1,11,1,NULL),(13,'КРУТО КЛАССНО ХОЧУ!','2025-12-25 12:42:36.221754','2025-12-25 12:42:36.221754',2,NULL,9,NULL),(14,'123','2025-12-25 13:56:37.205238','2025-12-25 13:56:37.205238',2,NULL,10,NULL),(15,'123','2025-12-25 13:56:46.518364','2025-12-25 13:56:46.518364',1,14,10,NULL);
/*!40000 ALTER TABLE `projects_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects_notification`
--

DROP TABLE IF EXISTS `projects_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `notification_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `comment_id` bigint DEFAULT NULL,
  `invitation_id` bigint DEFAULT NULL,
  `project_id` bigint DEFAULT NULL,
  `task_id` bigint DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `projects_notification_comment_id_0edcb49b_fk_projects_comment_id` (`comment_id`),
  KEY `projects_notificatio_invitation_id_5f637516_fk_projects_` (`invitation_id`),
  KEY `projects_notification_project_id_a60c74c8_fk_projects_project_id` (`project_id`),
  KEY `projects_notification_task_id_45f7c6b4_fk_projects_task_id` (`task_id`),
  KEY `projects_no_user_id_baa7c4_idx` (`user_id`,`is_read`,`created_at` DESC),
  CONSTRAINT `projects_notificatio_invitation_id_5f637516_fk_projects_` FOREIGN KEY (`invitation_id`) REFERENCES `projects_projectinvitation` (`id`),
  CONSTRAINT `projects_notification_comment_id_0edcb49b_fk_projects_comment_id` FOREIGN KEY (`comment_id`) REFERENCES `projects_comment` (`id`),
  CONSTRAINT `projects_notification_project_id_a60c74c8_fk_projects_project_id` FOREIGN KEY (`project_id`) REFERENCES `projects_project` (`id`),
  CONSTRAINT `projects_notification_task_id_45f7c6b4_fk_projects_task_id` FOREIGN KEY (`task_id`) REFERENCES `projects_task` (`id`),
  CONSTRAINT `projects_notification_user_id_8c506062_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects_notification`
--

LOCK TABLES `projects_notification` WRITE;
/*!40000 ALTER TABLE `projects_notification` DISABLE KEYS */;
INSERT INTO `projects_notification` VALUES (1,'comment_project','wrx666 оставил комментарий к вашему проекту \"Искусствох2\"',1,'2025-12-25 09:59:22.256928',5,NULL,8,NULL,1),(2,'comment_project','wrx666 оставил комментарий к вашему проекту \"Искусствох2\"',1,'2025-12-25 10:05:00.934832',7,NULL,8,NULL,1),(3,'comment_project','wrx666 оставил комментарий к вашему проекту \"Искусствох2\"',1,'2025-12-25 10:06:48.948301',9,NULL,8,NULL,1),(4,'comment_project','admin ответил на ваш комментарий к проекту \"Искусствох2\"',1,'2025-12-25 10:06:57.445483',10,NULL,8,NULL,2),(5,'invitation','Вас пригласили в проект \"12312\"',0,'2025-12-25 12:40:08.281221',NULL,3,9,NULL,2),(6,'comment_project','wrx666 оставил комментарий к вашему проекту \"Дизайн...\"',1,'2025-12-25 12:41:01.353523',11,NULL,1,NULL,1),(7,'comment_project','admin ответил на ваш комментарий к проекту \"Дизайн...\"',0,'2025-12-25 12:41:11.703053',12,NULL,1,NULL,2),(8,'comment_project','wrx666 оставил комментарий к вашему проекту \"12312\"',1,'2025-12-25 12:42:36.226740',13,NULL,9,NULL,1),(9,'invitation','Вас пригласили в проект \"12312\"',0,'2025-12-25 13:12:33.696172',NULL,4,9,NULL,2),(10,'invitation','Вас пригласили в проект \"12312\"',0,'2025-12-25 13:12:54.065927',NULL,5,9,NULL,2),(11,'invitation','Вас пригласили в проект \"музыка123\"',0,'2025-12-25 13:55:59.815068',NULL,6,10,NULL,2),(12,'comment_project','wrx666 оставил комментарий к вашему проекту \"музыка123\"',0,'2025-12-25 13:56:37.211222',14,NULL,10,NULL,1),(13,'comment_project','admin ответил на ваш комментарий к проекту \"музыка123\"',0,'2025-12-25 13:56:46.526769',15,NULL,10,NULL,2);
/*!40000 ALTER TABLE `projects_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects_project`
--

DROP TABLE IF EXISTS `projects_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects_project` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `section` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tags` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image_file` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `image_url` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `owner_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `projects_project_owner_id_b940de39_fk_auth_user_id` (`owner_id`),
  CONSTRAINT `projects_project_owner_id_b940de39_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects_project`
--

LOCK TABLES `projects_project` WRITE;
/*!40000 ALTER TABLE `projects_project` DISABLE KEYS */;
INSERT INTO `projects_project` VALUES (1,'Дизайн...','Дизайн','design','beginner, intermediate, advanced','projects/images/5782b760775cc240403824966a0d7595_processed.jpg','http://127.0.0.1:8000/media/projects/images/5782b760775cc240403824966a0d7595_processed.jpg','2025-12-24 23:43:09.444385','2025-12-25 02:05:52.886413',1),(2,'Музычка','Музычка','music','professional, collaboration, personal','projects/images/aa45f35f1f88673ce05f4751dedab1bd_processed.jpg','http://127.0.0.1:8000/media/projects/images/aa45f35f1f88673ce05f4751dedab1bd_processed.jpg','2025-12-25 03:08:54.455801','2025-12-25 03:08:54.455801',1),(3,'Фотографии','Фотографии','photography','advanced, solo, personal','projects/images/16c7a38c09bc16298389abcbc4d3e0e6_processed.jpg','http://127.0.0.1:8000/media/projects/images/16c7a38c09bc16298389abcbc4d3e0e6_processed.jpg','2025-12-25 03:10:20.557389','2025-12-25 03:10:20.557389',1),(4,'Видосики','Видосики','video','experimental, commercial','projects/images/859ddb999294e1c4bc8d94670a1644eb_processed.jpg','http://127.0.0.1:8000/media/projects/images/859ddb999294e1c4bc8d94670a1644eb_processed.jpg','2025-12-25 03:11:40.499924','2025-12-25 03:11:40.499924',1),(5,'Программирование','А если без прикола есть вариант с тобой побыть месяц вместе? Оплачу всякие приятности, если московская, то с радостью можем съехаться, без пошлостей, просто поживём вместе месяц, если понравлюсь, будем развивать наши отношения дальше. Ты мне без шуток нравишься, давно за тобой слежу. Скажи, пожалуйста, есть ли шанс на подобное? Могу написать в тг после стримчика. Целую','programming','solo, experimental, personal','projects/images/a322e05ef4f9c60bbc2948177e667401_processed.jpg','http://127.0.0.1:8000/media/projects/images/a322e05ef4f9c60bbc2948177e667401_processed.jpg','2025-12-25 03:12:48.498035','2025-12-25 09:34:22.449047',1),(6,'Писательство','Писательство','writing','beginner, collaboration, personal','projects/images/360b908681ae73277b499e20d96d9550_processed.jpg','http://127.0.0.1:8000/media/projects/images/360b908681ae73277b499e20d96d9550_processed.jpg','2025-12-25 03:13:39.680748','2025-12-25 03:13:39.681745',1),(7,'Искусство','Искусство','art','experimental, commercial','projects/images/dbe1c94be63fa384b313fd440a1a274e_processed.jpg','http://127.0.0.1:8000/media/projects/images/dbe1c94be63fa384b313fd440a1a274e_processed.jpg','2025-12-25 03:14:24.697387','2025-12-25 03:14:24.697387',1),(8,'Искусствох2','Искусствох2','art','beginner, collaboration, solo','projects/images/16f9c408029a8168b3ba0b73989f6d84_processed.jpg','http://127.0.0.1:8000/media/projects/images/16f9c408029a8168b3ba0b73989f6d84_processed.jpg','2025-12-25 03:15:25.125271','2025-12-25 03:15:25.125271',1),(9,'12312','123123','design','beginner, collaboration, commercial','projects/images/dbe1c94be63fa384b313fd440a1a274e_processed_7TCpkVi.jpg','http://127.0.0.1:8000/media/projects/images/dbe1c94be63fa384b313fd440a1a274e_processed_7TCpkVi.jpg','2025-12-25 11:59:16.620385','2025-12-25 11:59:16.620385',1),(10,'музыка123','музыка123','music','','projects/images/04910eb35ac194a5974d66383c298c93b47f78df_processed.jpg','http://127.0.0.1:8000/media/projects/images/04910eb35ac194a5974d66383c298c93b47f78df_processed.jpg','2025-12-25 13:55:45.546793','2025-12-25 13:55:45.546793',1);
/*!40000 ALTER TABLE `projects_project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects_projectfavorite`
--

DROP TABLE IF EXISTS `projects_projectfavorite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects_projectfavorite` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `project_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `projects_projectfavorite_user_id_project_id_a5a38b61_uniq` (`user_id`,`project_id`),
  KEY `projects_projectfavo_project_id_e600cc9d_fk_projects_` (`project_id`),
  CONSTRAINT `projects_projectfavo_project_id_e600cc9d_fk_projects_` FOREIGN KEY (`project_id`) REFERENCES `projects_project` (`id`),
  CONSTRAINT `projects_projectfavorite_user_id_54693676_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects_projectfavorite`
--

LOCK TABLES `projects_projectfavorite` WRITE;
/*!40000 ALTER TABLE `projects_projectfavorite` DISABLE KEYS */;
INSERT INTO `projects_projectfavorite` VALUES (1,'2025-12-25 01:36:18.063068',1,2),(3,'2025-12-25 03:08:58.116714',2,1),(4,'2025-12-25 03:10:22.278149',3,1),(5,'2025-12-25 03:11:44.621199',4,1),(6,'2025-12-25 03:12:53.028294',5,1),(7,'2025-12-25 03:13:41.290657',6,1),(8,'2025-12-25 03:14:26.121305',7,1),(9,'2025-12-25 03:15:26.482473',8,1),(10,'2025-12-25 13:56:26.683116',10,2);
/*!40000 ALTER TABLE `projects_projectfavorite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects_projectinvitation`
--

DROP TABLE IF EXISTS `projects_projectinvitation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects_projectinvitation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `invited_by_id` int NOT NULL,
  `invited_user_id` int NOT NULL,
  `project_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `projects_projectinvi_invited_by_id_18666dfb_fk_auth_user` (`invited_by_id`),
  KEY `projects_projectinvi_invited_user_id_0d5c9bbf_fk_auth_user` (`invited_user_id`),
  KEY `projects_projectinvi_project_id_c5f82e2a_fk_projects_` (`project_id`),
  CONSTRAINT `projects_projectinvi_invited_by_id_18666dfb_fk_auth_user` FOREIGN KEY (`invited_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `projects_projectinvi_invited_user_id_0d5c9bbf_fk_auth_user` FOREIGN KEY (`invited_user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `projects_projectinvi_project_id_c5f82e2a_fk_projects_` FOREIGN KEY (`project_id`) REFERENCES `projects_project` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects_projectinvitation`
--

LOCK TABLES `projects_projectinvitation` WRITE;
/*!40000 ALTER TABLE `projects_projectinvitation` DISABLE KEYS */;
INSERT INTO `projects_projectinvitation` VALUES (1,'cancelled','2025-12-25 01:33:55.124953','2025-12-25 01:34:11.485087',1,2,1),(2,'accepted','2025-12-25 01:34:24.943751','2025-12-25 01:34:34.857700',1,2,1),(3,'cancelled','2025-12-25 12:40:08.274983','2025-12-25 12:40:25.574980',1,2,9),(4,'cancelled','2025-12-25 13:12:33.691249','2025-12-25 13:12:45.825359',1,2,9),(5,'cancelled','2025-12-25 13:12:54.062107','2025-12-25 13:13:00.147670',1,2,9),(6,'accepted','2025-12-25 13:55:59.810078','2025-12-25 13:56:16.219944',1,2,10);
/*!40000 ALTER TABLE `projects_projectinvitation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects_projectparticipant`
--

DROP TABLE IF EXISTS `projects_projectparticipant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects_projectparticipant` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `joined_at` datetime(6) NOT NULL,
  `invited_by_id` int DEFAULT NULL,
  `project_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `projects_projectparticipant_project_id_user_id_39de0e6e_uniq` (`project_id`,`user_id`),
  KEY `projects_projectpart_invited_by_id_9fc9ce37_fk_auth_user` (`invited_by_id`),
  KEY `projects_projectparticipant_user_id_4c3c894d_fk_auth_user_id` (`user_id`),
  CONSTRAINT `projects_projectpart_invited_by_id_9fc9ce37_fk_auth_user` FOREIGN KEY (`invited_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `projects_projectpart_project_id_cd22ba8c_fk_projects_` FOREIGN KEY (`project_id`) REFERENCES `projects_project` (`id`),
  CONSTRAINT `projects_projectparticipant_user_id_4c3c894d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects_projectparticipant`
--

LOCK TABLES `projects_projectparticipant` WRITE;
/*!40000 ALTER TABLE `projects_projectparticipant` DISABLE KEYS */;
INSERT INTO `projects_projectparticipant` VALUES (3,'2025-12-25 01:34:34.855704',1,1,2),(4,'2025-12-25 13:56:16.212963',1,10,2);
/*!40000 ALTER TABLE `projects_projectparticipant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects_task`
--

DROP TABLE IF EXISTS `projects_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects_task` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `deadline` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `assignee_id` int DEFAULT NULL,
  `created_by_id` int NOT NULL,
  `project_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `projects_task_assignee_id_5061de72_fk_auth_user_id` (`assignee_id`),
  KEY `projects_task_created_by_id_3dc419bd_fk_auth_user_id` (`created_by_id`),
  KEY `projects_task_project_id_a1b987d6_fk_projects_project_id` (`project_id`),
  CONSTRAINT `projects_task_assignee_id_5061de72_fk_auth_user_id` FOREIGN KEY (`assignee_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `projects_task_created_by_id_3dc419bd_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `projects_task_project_id_a1b987d6_fk_projects_project_id` FOREIGN KEY (`project_id`) REFERENCES `projects_project` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects_task`
--

LOCK TABLES `projects_task` WRITE;
/*!40000 ALTER TABLE `projects_task` DISABLE KEYS */;
INSERT INTO `projects_task` VALUES (2,'123','12312','new','2025-12-25 13:41:00.000000','2025-12-25 09:50:08.560169','2025-12-25 09:50:08.560169',1,1,8);
/*!40000 ALTER TABLE `projects_task` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-29 20:08:50
