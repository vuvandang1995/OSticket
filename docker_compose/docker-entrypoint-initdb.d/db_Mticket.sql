-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: localhost    Database: mticket
-- ------------------------------------------------------
-- Server version 5.7.22-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `add_agents`
--

DROP TABLE IF EXISTS `add_agents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `add_agents` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `receiverid` int(11) NOT NULL,
  `senderid` int(11) NOT NULL,
  `ticketid` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `add_agents_receiverid_b093a0df_fk_agents_id` (`receiverid`),
  KEY `add_agents_senderid_0d02d852_fk_agents_id` (`senderid`),
  KEY `add_agents_ticketid_713054bf_fk_tickets_id` (`ticketid`),
  CONSTRAINT `add_agents_receiverid_b093a0df_fk_agents_id` FOREIGN KEY (`receiverid`) REFERENCES `agents` (`id`),
  CONSTRAINT `add_agents_senderid_0d02d852_fk_agents_id` FOREIGN KEY (`senderid`) REFERENCES `agents` (`id`),
  CONSTRAINT `add_agents_ticketid_713054bf_fk_tickets_id` FOREIGN KEY (`ticketid`) REFERENCES `tickets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `add_agents`
--

LOCK TABLES `add_agents` WRITE;
/*!40000 ALTER TABLE `add_agents` DISABLE KEYS */;
/*!40000 ALTER TABLE `add_agents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `agents`
--

DROP TABLE IF EXISTS `agents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agents` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fullname` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `receive_email` int(11) NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `admin` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `noti_noti` int(11) NOT NULL,
  `noti_chat` int(11) NOT NULL,
  `departmentid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `agents_departmentid_e50cabc0_fk_departments_id` (`departmentid`),
  CONSTRAINT `agents_departmentid_e50cabc0_fk_departments_id` FOREIGN KEY (`departmentid`) REFERENCES `departments` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agents`
--

LOCK TABLES `agents` WRITE;
/*!40000 ALTER TABLE `agents` DISABLE KEYS */;
INSERT INTO `agents` VALUES (1,'Administrator','admin@gmail.com','admin','0999999999',0,'meditech_2018',1,1,0,0,NULL),(2,'Nguyễn Văn Thao','thao.nguyenvan@meditech.vn','thaonv','0123456789',0,'meditech2017',0,1,0,0,1),(3,'Dương Văn Khoa','khoa.duongvan@meditech.vn','khoadv','0123456789',0,'meditech_2018',0,1,1,0,1),(4,'Nguyễn Việt Dũng','dung.nguyenviet@meditech.vn','dungnv','0123456789',0,'meditech_2018',0,1,0,0,1),(5,'Vũ Văn Đặng','dangdiendao@gmail.com','dangvv','0123456789',0,'dang123456',0,1,0,0,1),(6,'Đỗ Thị Mỹ Hạnh','hanh.dothimy@meditech.vn','hanhdtm','0123456789',0,'meditech_2018',0,1,1,0,1);
/*!40000 ALTER TABLE `agents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add permission',3,'add_permission'),(8,'Can change permission',3,'change_permission'),(9,'Can delete permission',3,'delete_permission'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add tickets',7,'add_tickets'),(20,'Can change tickets',7,'change_tickets'),(21,'Can delete tickets',7,'delete_tickets'),(22,'Can add agents',8,'add_agents'),(23,'Can change agents',8,'change_agents'),(24,'Can delete agents',8,'delete_agents'),(25,'Can add topics',9,'add_topics'),(26,'Can change topics',9,'change_topics'),(27,'Can delete topics',9,'delete_topics'),(28,'Can add users',10,'add_users'),(29,'Can change users',10,'change_users'),(30,'Can delete users',10,'delete_users'),(31,'Can add topic agent',11,'add_topicagent'),(32,'Can change topic agent',11,'change_topicagent'),(33,'Can delete topic agent',11,'delete_topicagent'),(34,'Can add add agents',12,'add_addagents'),(35,'Can change add agents',12,'change_addagents'),(36,'Can delete add agents',12,'delete_addagents'),(37,'Can add departments',13,'add_departments'),(38,'Can change departments',13,'change_departments'),(39,'Can delete departments',13,'delete_departments'),(40,'Can add ticket agent',14,'add_ticketagent'),(41,'Can change ticket agent',14,'change_ticketagent'),(42,'Can delete ticket agent',14,'delete_ticketagent'),(43,'Can add ticket log',15,'add_ticketlog'),(44,'Can change ticket log',15,'change_ticketlog'),(45,'Can delete ticket log',15,'delete_ticketlog'),(46,'Can add forward tickets',16,'add_forwardtickets'),(47,'Can change forward tickets',16,'change_forwardtickets'),(48,'Can delete forward tickets',16,'delete_forwardtickets');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `departments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
INSERT INTO `departments` VALUES (1,'Meditech','Công ty cổ phần Meditech');
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(12,'user','addagents'),(8,'user','agents'),(13,'user','departments'),(16,'user','forwardtickets'),(14,'user','ticketagent'),(15,'user','ticketlog'),(7,'user','tickets'),(11,'user','topicagent'),(9,'user','topics'),(10,'user','users');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2018-07-05 03:38:29.012723'),(2,'auth','0001_initial','2018-07-05 03:38:30.099252'),(3,'admin','0001_initial','2018-07-05 03:38:30.346083'),(4,'admin','0002_logentry_remove_auto_add','2018-07-05 03:38:30.361768'),(5,'contenttypes','0002_remove_content_type_name','2018-07-05 03:38:30.521361'),(6,'auth','0002_alter_permission_name_max_length','2018-07-05 03:38:30.606159'),(7,'auth','0003_alter_user_email_max_length','2018-07-05 03:38:30.634139'),(8,'auth','0004_alter_user_username_opts','2018-07-05 03:38:30.648471'),(9,'auth','0005_alter_user_last_login_null','2018-07-05 03:38:30.726199'),(10,'auth','0006_require_contenttypes_0002','2018-07-05 03:38:30.731507'),(11,'auth','0007_alter_validators_add_error_messages','2018-07-05 03:38:30.745725'),(12,'auth','0008_alter_user_username_max_length','2018-07-05 03:38:30.820522'),(13,'auth','0009_alter_user_last_name_max_length','2018-07-05 03:38:30.927694'),(14,'sessions','0001_initial','2018-07-05 03:38:31.011904'),(15,'user','0001_initial','2018-07-05 03:38:34.154154'),(16,'user','0002_remove_topics_type_send','2018-07-05 03:38:34.243941'),(17,'user','0003_auto_20180704_0906','2018-07-05 03:38:34.353366'),(18,'user','0004_auto_20180704_0911','2018-07-05 03:38:34.521093'),(19,'user','0005_auto_20180704_0916','2018-07-05 03:38:35.007336');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
INSERT INTO `django_session` VALUES ('1fmxf2vkghk13utnhujpvx7l9n9a4l0e','NmQwMDJjZTljNTA3MTdjMzkzNjVlZTA2MzhlZTdmNDc4ZjIzNWM5MTp7ImFnZW50IjoiZGFuZ3Z2In0=','2018-07-21 04:15:07.034385'),('4mup8dcjan9m94i95efjtbudwgedlkou','NTc1MGYwYTA5ODlmMGJiMTcyYWE5OTY0NzRkZDk1OTAxN2Q1MWQ3Mjp7fQ==','2018-07-19 10:28:37.747834'),('5o6l6zzetgzomhjec23gr1mhnfp04gpi','NmQwMDJjZTljNTA3MTdjMzkzNjVlZTA2MzhlZTdmNDc4ZjIzNWM5MTp7ImFnZW50IjoiZGFuZ3Z2In0=','2018-07-21 03:17:16.246079'),('6zcxt5afyjtt6zr6gsrwkxb9b8yc8jhk','NmQwMDJjZTljNTA3MTdjMzkzNjVlZTA2MzhlZTdmNDc4ZjIzNWM5MTp7ImFnZW50IjoiZGFuZ3Z2In0=','2018-07-19 13:15:49.629813'),('c23ucwqa33h1k1fl96qsmu12b8g1cseg','NTc1MGYwYTA5ODlmMGJiMTcyYWE5OTY0NzRkZDk1OTAxN2Q1MWQ3Mjp7fQ==','2018-07-20 10:38:44.213738'),('d4a0vsljg3hcxre14nmk6zbx0hz4ov3u','NjYwNTZkOWI0MzAxODE3ZjA1Y2I0NTcyMmE5ZjZjMTgwN2ZkMDFiYTp7InVzZXIiOiJkYW5ndnYifQ==','2018-07-19 06:47:07.185238'),('e8dll4pxggwumefcn0t51oqyk3n7omjy','NjYwNTZkOWI0MzAxODE3ZjA1Y2I0NTcyMmE5ZjZjMTgwN2ZkMDFiYTp7InVzZXIiOiJkYW5ndnYifQ==','2018-07-19 16:18:14.802797'),('ekrp27pakihz675zitvtmvegu0rybgok','NjYwNTZkOWI0MzAxODE3ZjA1Y2I0NTcyMmE5ZjZjMTgwN2ZkMDFiYTp7InVzZXIiOiJkYW5ndnYifQ==','2018-07-19 23:27:39.603558'),('eskcykxj9wriyw9c9gadmkuvoybkl2n7','MDI2ZTg5ZjIwYjlmOTExOGU4ZWU0MmQwNGM3MjNmYWQ1Zjk3M2Q5YTp7InVzZXIiOiJ0cmFuZ3NpZXVjdXRlIn0=','2018-07-19 04:51:17.703531'),('i0rjibmlow3alshaegdolfuxoth1u0r8','NTc1MGYwYTA5ODlmMGJiMTcyYWE5OTY0NzRkZDk1OTAxN2Q1MWQ3Mjp7fQ==','2018-07-20 07:17:01.549899'),('ndleaxsvs04tg5mgo5wjyapgaw96vji0','NjYwNTZkOWI0MzAxODE3ZjA1Y2I0NTcyMmE5ZjZjMTgwN2ZkMDFiYTp7InVzZXIiOiJkYW5ndnYifQ==','2018-07-20 23:35:49.185378'),('uw3vd9n6mamt6eh6okf10ajhemqyilc0','NjYwNTZkOWI0MzAxODE3ZjA1Y2I0NTcyMmE5ZjZjMTgwN2ZkMDFiYTp7InVzZXIiOiJkYW5ndnYifQ==','2018-07-20 07:49:07.012929'),('wm8dx8w6ym42ghutw2z6kora2pkoc98h','NTQzNWYzOTM3NWVlMzgyYmMxNDk3NDdiM2E2ZTc4OWE2NzUyYTJhYjp7InVzZXIiOiJkdWMifQ==','2018-07-19 04:52:51.316480');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forward_tickets`
--

DROP TABLE IF EXISTS `forward_tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forward_tickets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `receiverid` int(11) NOT NULL,
  `senderid` int(11) NOT NULL,
  `ticketid` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `forward_tickets_receiverid_00cdb591_fk_agents_id` (`receiverid`),
  KEY `forward_tickets_senderid_80ab19af_fk_agents_id` (`senderid`),
  KEY `forward_tickets_ticketid_49135b73_fk_tickets_id` (`ticketid`),
  CONSTRAINT `forward_tickets_receiverid_00cdb591_fk_agents_id` FOREIGN KEY (`receiverid`) REFERENCES `agents` (`id`),
  CONSTRAINT `forward_tickets_senderid_80ab19af_fk_agents_id` FOREIGN KEY (`senderid`) REFERENCES `agents` (`id`),
  CONSTRAINT `forward_tickets_ticketid_49135b73_fk_tickets_id` FOREIGN KEY (`ticketid`) REFERENCES `tickets` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forward_tickets`
--

LOCK TABLES `forward_tickets` WRITE;
/*!40000 ALTER TABLE `forward_tickets` DISABLE KEYS */;
/*!40000 ALTER TABLE `forward_tickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket_agent`
--

DROP TABLE IF EXISTS `ticket_agent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ticket_agent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `agentid` int(11) NOT NULL,
  `ticketid` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ticket_agent_agentid_d6a34996_fk_agents_id` (`agentid`),
  KEY `ticket_agent_ticketid_14699b3f_fk_tickets_id` (`ticketid`),
  CONSTRAINT `ticket_agent_agentid_d6a34996_fk_agents_id` FOREIGN KEY (`agentid`) REFERENCES `agents` (`id`),
  CONSTRAINT `ticket_agent_ticketid_14699b3f_fk_tickets_id` FOREIGN KEY (`ticketid`) REFERENCES `tickets` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket_agent`
--

LOCK TABLES `ticket_agent` WRITE;
/*!40000 ALTER TABLE `ticket_agent` DISABLE KEYS */;
INSERT INTO `ticket_agent` VALUES (1,4,4),(2,5,5),(3,5,8),(4,4,6),(5,5,7);
/*!40000 ALTER TABLE `ticket_agent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket_log`
--

DROP TABLE IF EXISTS `ticket_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ticket_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` date NOT NULL,
  `time` time(6) NOT NULL,
  `agentid` int(11) DEFAULT NULL,
  `ticketid` int(11) NOT NULL,
  `userid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ticket_log_agentid_6c99614a_fk_agents_id` (`agentid`),
  KEY `ticket_log_ticketid_7fd3b154_fk_tickets_id` (`ticketid`),
  KEY `ticket_log_userid_5425f04a_fk_users_id` (`userid`),
  CONSTRAINT `ticket_log_agentid_6c99614a_fk_agents_id` FOREIGN KEY (`agentid`) REFERENCES `agents` (`id`),
  CONSTRAINT `ticket_log_ticketid_7fd3b154_fk_tickets_id` FOREIGN KEY (`ticketid`) REFERENCES `tickets` (`id`),
  CONSTRAINT `ticket_log_userid_5425f04a_fk_users_id` FOREIGN KEY (`userid`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket_log`
--

LOCK TABLES `ticket_log` WRITE;
/*!40000 ALTER TABLE `ticket_log` DISABLE KEYS */;
INSERT INTO `ticket_log` VALUES (1,'create ticket','2018-07-05','04:53:54.151583',NULL,1,3),(2,'create ticket','2018-07-05','04:54:10.741025',NULL,2,2),(4,'create ticket','2018-07-05','05:18:23.732152',NULL,4,4),(5,'assign ticket','2018-07-05','06:42:14.694553',4,4,NULL),(6,'done ticket','2018-07-05','06:43:08.424407',4,4,NULL),(7,'done ticket','2018-07-05','06:43:22.898844',4,4,NULL),(8,'done ticket','2018-07-05','06:43:40.793649',4,4,NULL),(9,'create ticket','2018-07-05','06:47:19.516748',NULL,5,1),(10,'assign ticket','2018-07-05','06:47:26.261407',5,5,NULL),(11,'done ticket','2018-07-05','06:47:57.645260',5,5,NULL),(12,'done ticket','2018-07-05','08:02:58.077143',5,5,NULL),(13,'done ticket','2018-07-05','08:03:08.257365',5,5,NULL),(14,'done ticket','2018-07-05','09:25:27.010259',5,5,NULL),(15,'done ticket','2018-07-05','09:25:31.543212',5,5,NULL),(16,'create ticket','2018-07-05','10:11:30.920050',NULL,6,4),(17,'done ticket','2018-07-05','13:16:04.930487',5,5,NULL),(18,'done ticket','2018-07-05','13:16:23.651739',5,5,NULL),(19,'create ticket','2018-07-05','13:16:47.309718',NULL,7,1),(20,'done ticket','2018-07-05','13:42:38.144055',5,5,NULL),(21,'done ticket','2018-07-05','16:02:53.564105',5,5,NULL),(22,'done ticket','2018-07-05','16:06:16.437942',5,5,NULL),(23,'create ticket','2018-07-05','16:18:32.582164',NULL,8,1),(24,'assign ticket','2018-07-06','03:42:04.026099',5,8,NULL),(25,'assign ticket','2018-07-06','10:25:51.003672',4,6,NULL),(26,'received ticket forward from (admin)admin','2018-07-06','16:03:51.658445',5,7,NULL),(27,'done ticket','2018-07-06','23:35:25.490341',5,8,NULL);
/*!40000 ALTER TABLE `ticket_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tickets`
--

DROP TABLE IF EXISTS `tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tickets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `chat` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `content` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` int(11) NOT NULL,
  `datestart` datetime(6) NOT NULL,
  `dateend` datetime(6) NOT NULL,
  `attach` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sender` int(11) NOT NULL,
  `topicid` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tickets_sender_75e8a3b8_fk_users_id` (`sender`),
  KEY `tickets_topicid_fe95e42a_fk_topics_id` (`topicid`),
  CONSTRAINT `tickets_sender_75e8a3b8_fk_users_id` FOREIGN KEY (`sender`) REFERENCES `users` (`id`),
  CONSTRAINT `tickets_topicid_fe95e42a_fk_topics_id` FOREIGN KEY (`topicid`) REFERENCES `topics` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tickets`
--

LOCK TABLES `tickets` WRITE;
/*!40000 ALTER TABLE `tickets` DISABLE KEYS */;
INSERT INTO `tickets` VALUES (1,'hế lô',NULL,'aaa',0,'2018-07-05 04:53:54.141844','2018-07-08 04:53:54.141854','',3,5),(2,'Ăn uống',NULL,'Đói quá, được đi ăn chưa ạ?',0,'2018-07-05 04:54:10.726625','2018-07-08 04:54:10.726635','',2,6),(4,'Test gửi ảnh',NULL,'Gửi thử 1 ảnh để test',2,'2018-07-05 05:18:23.724324','2018-07-08 05:18:23.724334','photos/751d7512-c9e7-44a5-be56-6b1ff9096adf_pP4IyDB.png',4,4),(5,'a',NULL,'a',1,'2018-07-05 06:47:19.507441','2018-07-08 06:47:19.507451','',1,4),(6,'Test gửi ảnh',NULL,'Test gửi ảnh',1,'2018-07-05 10:11:30.907359','2018-07-08 10:11:30.907370','photos/751d7512-c9e7-44a5-be56-6b1ff9096adf_kyFtsTk.png',4,4),(7,'Test realtime',NULL,'a',1,'2018-07-05 13:16:47.296612','2018-07-08 13:16:47.296622','',1,4),(8,'Đặng',NULL,'Đăng ơi',2,'2018-07-05 16:18:32.571499','2018-07-08 16:18:32.571508','',1,4);
/*!40000 ALTER TABLE `tickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topic_agent`
--

DROP TABLE IF EXISTS `topic_agent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topic_agent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `agentid` int(11) NOT NULL,
  `topicid` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `topic_agent_agentid_9d517e08_fk_agents_id` (`agentid`),
  KEY `topic_agent_topicid_9395a1d2_fk_topics_id` (`topicid`),
  CONSTRAINT `topic_agent_agentid_9d517e08_fk_agents_id` FOREIGN KEY (`agentid`) REFERENCES `agents` (`id`),
  CONSTRAINT `topic_agent_topicid_9395a1d2_fk_topics_id` FOREIGN KEY (`topicid`) REFERENCES `topics` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topic_agent`
--

LOCK TABLES `topic_agent` WRITE;
/*!40000 ALTER TABLE `topic_agent` DISABLE KEYS */;
INSERT INTO `topic_agent` VALUES (1,2,2),(2,3,3),(3,4,4),(4,5,4),(5,2,5),(6,6,6);
/*!40000 ALTER TABLE `topic_agent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topics`
--

DROP TABLE IF EXISTS `topics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` int(11) NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `departmentid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `topics_departmentid_d005f93d_fk_departments_id` (`departmentid`),
  CONSTRAINT `topics_departmentid_d005f93d_fk_departments_id` FOREIGN KEY (`departmentid`) REFERENCES `departments` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topics`
--

LOCK TABLES `topics` WRITE;
/*!40000 ALTER TABLE `topics` DISABLE KEYS */;
INSERT INTO `topics` VALUES (1,'Other',1,'other',NULL),(2,'Private Cloud ',0,'Hỗ trợ hệ thống Private Cloud',1),(3,'Monitor System ',0,'Phát triển, triển khai hệ thống giám sát',1),(4,'Dev Department',0,'Phát triển sản phẩm của team dev',1),(5,'Research Department',0,'Vấn đề của bộ phận nghiêm cứu ',1),(6,'Administration',0,'Hành chính, nhân sự, chính sách ',1);
/*!40000 ALTER TABLE `topics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fullname` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `receive_email` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `created` datetime(6) NOT NULL,
  `noti_noti` int(11) NOT NULL,
  `noti_chat` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Vũ Văn Đặng','dangdiendao@gmail.com','dangvv','123456','0914185983',0,1,'2018-07-05 04:28:27.422012',0,0),(2,'Nguyễn Trang','nguyenhuyentrang1996@gmail.com','trangsieucute','trang1234','0911114924',1,1,'2018-07-05 04:50:51.735479',0,0),(3,'Nguyễn Minh Đức','nh0x.xyteen1@gmail.com','duc','123456','01683165445',1,1,'2018-07-05 04:51:39.723839',0,0),(4,'Nguyễn Việt Dũng','sinionth@gmail.com','dung1101','123456','0123456789',1,1,'2018-07-05 05:17:17.580083',1,0);
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

-- Dump completed on 2018-07-08 13:27:19