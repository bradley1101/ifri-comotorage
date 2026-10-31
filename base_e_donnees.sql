-- =====================================================================
--  IFRI Comotorage — base de données MySQL / MariaDB
--  Structure complète (tables Django + applications) et données de démo.
--
--  Import :   mysql -u root -p < base_e_donnees.sql
--  Comptes de démo (mot de passe : ifri2025demo) :
--     koffi, rita, marc (conducteurs) — awa, jean, ella (passagers)
--  Les dates des trajets de démo sont relatives au jour de génération ;
--  pour des dates à jour, préférez :  python manage.py seed_demo
-- =====================================================================
CREATE DATABASE IF NOT EXISTS comotorage CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE comotorage;
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

/*M!999999\- enable the sandbox mode */ 
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
INSERT INTO `auth_permission` VALUES
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',2,'add_permission'),
(6,'Can change permission',2,'change_permission'),
(7,'Can delete permission',2,'delete_permission'),
(8,'Can view permission',2,'view_permission'),
(9,'Can add group',3,'add_group'),
(10,'Can change group',3,'change_group'),
(11,'Can delete group',3,'delete_group'),
(12,'Can view group',3,'view_group'),
(13,'Can add content type',4,'add_contenttype'),
(14,'Can change content type',4,'change_contenttype'),
(15,'Can delete content type',4,'delete_contenttype'),
(16,'Can view content type',4,'view_contenttype'),
(17,'Can add session',5,'add_session'),
(18,'Can change session',5,'change_session'),
(19,'Can delete session',5,'delete_session'),
(20,'Can view session',5,'view_session'),
(21,'Can add user',6,'add_user'),
(22,'Can change user',6,'change_user'),
(23,'Can delete user',6,'delete_user'),
(24,'Can view user',6,'view_user'),
(25,'Can add véhicule',7,'add_vehicule'),
(26,'Can change véhicule',7,'change_vehicule'),
(27,'Can delete véhicule',7,'delete_vehicule'),
(28,'Can view véhicule',7,'view_vehicule'),
(29,'Can add reservation',8,'add_reservation'),
(30,'Can change reservation',8,'change_reservation'),
(31,'Can delete reservation',8,'delete_reservation'),
(32,'Can view reservation',8,'view_reservation'),
(33,'Can add trajet',9,'add_trajet'),
(34,'Can change trajet',9,'change_trajet'),
(35,'Can delete trajet',9,'delete_trajet'),
(36,'Can view trajet',9,'view_trajet'),
(37,'Can add avis',10,'add_avis'),
(38,'Can change avis',10,'change_avis'),
(39,'Can delete avis',10,'delete_avis'),
(40,'Can view avis',10,'view_avis'),
(41,'Can add conversation',11,'add_conversation'),
(42,'Can change conversation',11,'change_conversation'),
(43,'Can delete conversation',11,'delete_conversation'),
(44,'Can view conversation',11,'view_conversation'),
(45,'Can add message',12,'add_message'),
(46,'Can change message',12,'change_message'),
(47,'Can delete message',12,'delete_message'),
(48,'Can view message',12,'view_message'),
(49,'Can add notification',13,'add_notification'),
(50,'Can change notification',13,'change_notification'),
(51,'Can delete notification',13,'delete_notification'),
(52,'Can view notification',13,'view_notification');
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `avis_avis` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `note` smallint(5) unsigned NOT NULL CHECK (`note` >= 0),
  `commentaire` longtext NOT NULL,
  `cree_le` datetime(6) NOT NULL,
  `auteur_id` bigint(20) NOT NULL,
  `cible_id` bigint(20) NOT NULL,
  `trajet_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `un_avis_par_personne_et_trajet` (`auteur_id`,`cible_id`,`trajet_id`),
  KEY `avis_avis_cible_id_2c5f5292_fk_users_user_id` (`cible_id`),
  KEY `avis_avis_trajet_id_8b58f68b_fk_trajets_trajet_id` (`trajet_id`),
  CONSTRAINT `avis_avis_auteur_id_1f0cdfb6_fk_users_user_id` FOREIGN KEY (`auteur_id`) REFERENCES `users_user` (`id`),
  CONSTRAINT `avis_avis_cible_id_2c5f5292_fk_users_user_id` FOREIGN KEY (`cible_id`) REFERENCES `users_user` (`id`),
  CONSTRAINT `avis_avis_trajet_id_8b58f68b_fk_trajets_trajet_id` FOREIGN KEY (`trajet_id`) REFERENCES `trajets_trajet` (`id`),
  CONSTRAINT `note_entre_1_et_5` CHECK (`note` >= 1 and `note` <= 5)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
INSERT INTO `avis_avis` VALUES
(1,5,'Très ponctuel, conduite prudente.','2026-10-31 19:38:16.910792',4,1,9),
(2,4,'Bonne ambiance, un peu de retard au départ.','2026-10-31 19:38:16.911566',6,1,9),
(3,5,'Passagère au rendez-vous à l\'heure.','2026-10-31 19:38:16.912093',1,4,9);
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
INSERT INTO `django_content_type` VALUES
(1,'admin','logentry'),
(3,'auth','group'),
(2,'auth','permission'),
(10,'avis','avis'),
(4,'contenttypes','contenttype'),
(11,'messaging','conversation'),
(12,'messaging','message'),
(13,'notifications','notification'),
(7,'profil','vehicule'),
(5,'sessions','session'),
(8,'trajets','reservation'),
(9,'trajets','trajet'),
(6,'users','user');
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
INSERT INTO `django_migrations` VALUES
(1,'contenttypes','0001_initial','2026-10-31 19:38:14.873822'),
(2,'contenttypes','0002_remove_content_type_name','2026-10-31 19:38:14.886102'),
(3,'auth','0001_initial','2026-10-31 19:38:14.921401'),
(4,'auth','0002_alter_permission_name_max_length','2026-10-31 19:38:14.927990'),
(5,'auth','0003_alter_user_email_max_length','2026-10-31 19:38:14.931092'),
(6,'auth','0004_alter_user_username_opts','2026-10-31 19:38:14.933715'),
(7,'auth','0005_alter_user_last_login_null','2026-10-31 19:38:14.936423'),
(8,'auth','0006_require_contenttypes_0002','2026-10-31 19:38:14.937929'),
(9,'auth','0007_alter_validators_add_error_messages','2026-10-31 19:38:14.941061'),
(10,'auth','0008_alter_user_username_max_length','2026-10-31 19:38:14.944238'),
(11,'auth','0009_alter_user_last_name_max_length','2026-10-31 19:38:14.947356'),
(12,'auth','0010_alter_group_name_max_length','2026-10-31 19:38:14.953154'),
(13,'auth','0011_update_proxy_permissions','2026-10-31 19:38:14.956379'),
(14,'auth','0012_alter_user_first_name_max_length','2026-10-31 19:38:14.959379'),
(15,'users','0001_initial','2026-10-31 19:38:14.997277'),
(16,'admin','0001_initial','2026-10-31 19:38:15.012871'),
(17,'admin','0002_logentry_remove_auto_add','2026-10-31 19:38:15.020716'),
(18,'admin','0003_logentry_add_action_flag_choices','2026-10-31 19:38:15.025055'),
(19,'trajets','0001_initial','2026-10-31 19:38:15.032690'),
(20,'avis','0001_initial','2026-10-31 19:38:15.036115'),
(21,'avis','0002_initial','2026-10-31 19:38:15.091504'),
(22,'messaging','0001_initial','2026-10-31 19:38:15.097635'),
(23,'messaging','0002_initial','2026-10-31 19:38:15.213974'),
(24,'notifications','0001_initial','2026-10-31 19:38:15.218711'),
(25,'notifications','0002_initial','2026-10-31 19:38:15.237341'),
(26,'profil','0001_initial','2026-10-31 19:38:15.241718'),
(27,'profil','0002_initial','2026-10-31 19:38:15.259079'),
(28,'sessions','0001_initial','2026-10-31 19:38:15.268525'),
(29,'trajets','0002_initial','2026-10-31 19:38:15.348853');
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `messaging_conversation` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `mis_a_jour` datetime(6) NOT NULL,
  `trajet_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `messaging_conversation_trajet_id_3feda48b_fk_trajets_trajet_id` (`trajet_id`),
  CONSTRAINT `messaging_conversation_trajet_id_3feda48b_fk_trajets_trajet_id` FOREIGN KEY (`trajet_id`) REFERENCES `trajets_trajet` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
INSERT INTO `messaging_conversation` VALUES
(1,'2026-10-31 19:38:16.914580',1);
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `messaging_conversation_participants` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `conversation_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `messaging_conversation_p_conversation_id_user_id_74726b68_uniq` (`conversation_id`,`user_id`),
  KEY `messaging_conversati_user_id_d4f41769_fk_users_use` (`user_id`),
  CONSTRAINT `messaging_conversati_conversation_id_890e9e37_fk_messaging` FOREIGN KEY (`conversation_id`) REFERENCES `messaging_conversation` (`id`),
  CONSTRAINT `messaging_conversati_user_id_d4f41769_fk_users_use` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
INSERT INTO `messaging_conversation_participants` VALUES
(1,1,1),
(2,1,4);
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `messaging_message` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `contenu` longtext NOT NULL,
  `envoye_le` datetime(6) NOT NULL,
  `lu` tinyint(1) NOT NULL,
  `auteur_id` bigint(20) NOT NULL,
  `conversation_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `messaging_message_auteur_id_c6e9c1dc_fk_users_user_id` (`auteur_id`),
  KEY `messaging_message_conversation_id_3db4d3d1_fk_messaging` (`conversation_id`),
  CONSTRAINT `messaging_message_auteur_id_c6e9c1dc_fk_users_user_id` FOREIGN KEY (`auteur_id`) REFERENCES `users_user` (`id`),
  CONSTRAINT `messaging_message_conversation_id_3db4d3d1_fk_messaging` FOREIGN KEY (`conversation_id`) REFERENCES `messaging_conversation` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
INSERT INTO `messaging_message` VALUES
(1,'Bonjour Koffi, je serai à la station Total vers 7h20.','2026-10-31 19:38:16.916128',1,4,1),
(2,'Parfait, je pars à 7h30 pile. Voiture grise.','2026-10-31 19:38:16.917009',0,1,1),
(3,'Super, merci !','2026-10-31 19:38:16.917788',1,4,1);
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications_notification` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `type` varchar(12) NOT NULL,
  `texte` varchar(255) NOT NULL,
  `lien` varchar(255) NOT NULL,
  `lue` tinyint(1) NOT NULL,
  `cree_le` datetime(6) NOT NULL,
  `destinataire_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `notifications_notifi_destinataire_id_04593f78_fk_users_use` (`destinataire_id`),
  CONSTRAINT `notifications_notifi_destinataire_id_04593f78_fk_users_use` FOREIGN KEY (`destinataire_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
INSERT INTO `notifications_notification` VALUES
(1,'reservation','Awa Sossa demande 1 place(s) pour Carrefour Godomey → IFRI — UAC Abomey-Calavi.','/trajets/1/',0,'2026-10-31 19:38:16.884120',1),
(2,'acceptee','Koffi Adjovi a accepté votre réservation pour Carrefour Godomey → IFRI — UAC Abomey-Calavi.','/trajets/1/',0,'2026-10-31 19:38:16.887737',4),
(3,'reservation','Jean Houngbo demande 1 place(s) pour Carrefour Godomey → IFRI — UAC Abomey-Calavi.','/trajets/1/',0,'2026-10-31 19:38:16.893352',1),
(4,'reservation','Ella Zinsou demande 1 place(s) pour Calavi Kpota → IFRI — UAC Abomey-Calavi.','/trajets/3/',0,'2026-10-31 19:38:16.898363',3),
(5,'acceptee','Marc Dossou a accepté votre réservation pour Calavi Kpota → IFRI — UAC Abomey-Calavi.','/trajets/3/',0,'2026-10-31 19:38:16.902665',6),
(6,'reservation','Awa Sossa demande 1 place(s) pour Cotonou — Étoile Rouge → IFRI — UAC Abomey-Calavi.','/trajets/2/',0,'2026-10-31 19:38:16.907786',2);
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `profil_vehicule` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `marque` varchar(40) NOT NULL,
  `modele` varchar(40) NOT NULL,
  `couleur` varchar(30) NOT NULL,
  `places` smallint(5) unsigned NOT NULL CHECK (`places` >= 0),
  `immatriculation` varchar(15) NOT NULL,
  `proprietaire_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `proprietaire_id` (`proprietaire_id`),
  CONSTRAINT `profil_vehicule_proprietaire_id_74bbf6df_fk_users_user_id` FOREIGN KEY (`proprietaire_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
INSERT INTO `profil_vehicule` VALUES
(1,'Toyota','Corolla','grise',3,'',1),
(2,'Suzuki','Swift','rouge',3,'',2),
(3,'Bajaj','Boxer (moto)','noire',1,'',3);
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `trajets_reservation` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `places` smallint(5) unsigned NOT NULL CHECK (`places` >= 0),
  `message` varchar(300) NOT NULL,
  `statut` varchar(10) NOT NULL,
  `cree_le` datetime(6) NOT NULL,
  `passager_id` bigint(20) NOT NULL,
  `trajet_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `une_reservation_par_trajet` (`trajet_id`,`passager_id`),
  KEY `trajets_reservation_passager_id_da931d68_fk_users_user_id` (`passager_id`),
  CONSTRAINT `trajets_reservation_passager_id_da931d68_fk_users_user_id` FOREIGN KEY (`passager_id`) REFERENCES `users_user` (`id`),
  CONSTRAINT `trajets_reservation_trajet_id_1d4330ee_fk_trajets_trajet_id` FOREIGN KEY (`trajet_id`) REFERENCES `trajets_trajet` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
INSERT INTO `trajets_reservation` VALUES
(1,1,'Je serai à la station.','confirmee','2026-10-31 19:38:16.877091',4,1),
(2,1,'Bonjour, il reste une place ?','en_attente','2026-10-31 19:38:16.891798',5,1),
(3,1,'','confirmee','2026-10-31 19:38:16.897137',6,3),
(4,1,'','en_attente','2026-10-31 19:38:16.905754',4,2),
(5,1,'','confirmee','2026-10-31 19:38:16.908914',4,9),
(6,1,'','confirmee','2026-10-31 19:38:16.909465',6,9);
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `trajets_trajet` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `lieu_depart` varchar(120) NOT NULL,
  `lat_depart` decimal(9,6) NOT NULL,
  `lng_depart` decimal(9,6) NOT NULL,
  `lieu_arrivee` varchar(120) NOT NULL,
  `lat_arrivee` decimal(9,6) NOT NULL,
  `lng_arrivee` decimal(9,6) NOT NULL,
  `date_depart` datetime(6) NOT NULL,
  `places_total` smallint(5) unsigned NOT NULL CHECK (`places_total` >= 0),
  `prix` int(10) unsigned NOT NULL CHECK (`prix` >= 0),
  `description` longtext NOT NULL,
  `bagages` tinyint(1) NOT NULL,
  `statut` varchar(8) NOT NULL,
  `cree_le` datetime(6) NOT NULL,
  `conducteur_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `trajets_trajet_conducteur_id_b6b64490_fk_users_user_id` (`conducteur_id`),
  KEY `trajets_tra_statut_bec530_idx` (`statut`,`date_depart`),
  CONSTRAINT `trajets_trajet_conducteur_id_b6b64490_fk_users_user_id` FOREIGN KEY (`conducteur_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
INSERT INTO `trajets_trajet` VALUES
(1,'Carrefour Godomey',6.386600,2.349700,'IFRI — UAC Abomey-Calavi',6.418300,2.341700,'2026-11-01 06:30:00.000000',3,300,'Départ devant la station Total. Je passe par Zogbadjè.',1,'ouvert','2026-10-31 19:38:16.867618',1),
(2,'Cotonou — Étoile Rouge',6.374500,2.412000,'IFRI — UAC Abomey-Calavi',6.418300,2.341700,'2026-11-01 05:00:00.000000',3,500,'Clim, ponctuelle. Merci d\'être à l\'heure.',1,'ouvert','2026-10-31 19:38:16.868384',2),
(3,'Calavi Kpota',6.448500,2.355000,'IFRI — UAC Abomey-Calavi',6.418300,2.341700,'2026-11-01 06:30:00.000000',1,200,'Moto, casque fourni.',1,'complet','2026-10-31 19:38:16.869039',3),
(4,'IFRI — UAC Abomey-Calavi',6.418300,2.341700,'Carrefour Godomey',6.386600,2.349700,'2026-11-01 16:30:00.000000',3,300,'Retour après les cours.',1,'ouvert','2026-10-31 19:38:16.869665',1),
(5,'Akpakpa — Carrefour Sègbèya',6.361500,2.451000,'IFRI — UAC Abomey-Calavi',6.418300,2.341700,'2026-11-02 05:00:00.000000',3,600,'',1,'ouvert','2026-10-31 19:38:16.870144',2),
(6,'Fidjrossè Plage',6.357500,2.365000,'IFRI — UAC Abomey-Calavi',6.418300,2.341700,'2026-11-03 06:30:00.000000',3,500,'',1,'ouvert','2026-10-31 19:38:16.870600',1),
(7,'Togba',6.456000,2.315000,'IFRI — UAC Abomey-Calavi',6.418300,2.341700,'2026-11-02 07:00:00.000000',1,200,'',1,'ouvert','2026-10-31 19:38:16.871060',3),
(8,'IFRI — UAC Abomey-Calavi',6.418300,2.341700,'Cadjèhoun',6.357000,2.390000,'2026-11-02 17:00:00.000000',3,500,'Je peux déposer à Vèdoko.',1,'ouvert','2026-10-31 19:38:16.871540',2),
(9,'Carrefour Godomey',6.386600,2.349700,'IFRI — UAC Abomey-Calavi',6.418300,2.341700,'2026-10-27 19:00:00.000000',3,300,'',1,'ouvert','2026-10-31 19:38:16.908479',1);
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  `telephone` varchar(20) NOT NULL,
  `role` varchar(12) NOT NULL,
  `filiere` varchar(8) NOT NULL,
  `bio` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
INSERT INTO `users_user` VALUES
(1,'pbkdf2_sha256$1000000$xnGkfBLaNWalxMkjVRic7t$oMv2Qbvd8ScgHVgRp49BnzpPghU36/TK3/XJAnU0oD0=',NULL,0,'koffi','Koffi','Adjovi',0,1,'2026-10-31 19:38:15.781197','koffi@ifri-demo.bj','+229 01 00 00 00','conducteur','SEIOT','Étudiant(e) en SEIOT à l\'IFRI.'),
(2,'pbkdf2_sha256$1000000$DnT0OsXT1Z8V05lnoo1Wt1$IE+DWQWc+ZhckJ9KBn5OV6pOXn0h0TnDaDRnzO6iUgc=',NULL,0,'rita','Rita','Agossou',0,1,'2026-10-31 19:38:15.956816','rita@ifri-demo.bj','+229 01 00 00 00','les_deux','GL','Étudiant(e) en GL à l\'IFRI.'),
(3,'pbkdf2_sha256$1000000$LqCqIFRexec7K94FzRpeIk$/bTHQTAKChVEx7VTD2tP1G0vxxU32waHuOqsWxUUWBY=',NULL,0,'marc','Marc','Dossou',0,1,'2026-10-31 19:38:16.132488','marc@ifri-demo.bj','+229 01 00 00 00','conducteur','IA','Étudiant(e) en IA à l\'IFRI.'),
(4,'pbkdf2_sha256$1000000$DjQamb7aD1cKXgvhVjbTBr$2wLHWRqGdF588+tsuacPSDWYCIGPCkSD4eVCkLtedUw=',NULL,0,'awa','Awa','Sossa',0,1,'2026-10-31 19:38:16.334457','awa@ifri-demo.bj','+229 01 00 00 00','passager','SEIOT','Étudiant(e) en SEIOT à l\'IFRI.'),
(5,'pbkdf2_sha256$1000000$PWvEgLGkBIosnD2XRy0StO$YD/CSfgWavN7EL/Dbgu4Sm/D2xFnC/CD3sqy6ohB5bg=',NULL,0,'jean','Jean','Houngbo',0,1,'2026-10-31 19:38:16.525878','jean@ifri-demo.bj','+229 01 00 00 00','passager','SI','Étudiant(e) en SI à l\'IFRI.'),
(6,'pbkdf2_sha256$1000000$SiC1qDDOvLHqaXGHKw6OsR$FLP1P2WtnUt2QEEwFSympu7+2JuJ3RRkOokAi6M/kLs=',NULL,0,'ella','Ella','Zinsou',0,1,'2026-10-31 19:38:16.698983','ella@ifri-demo.bj','+229 01 00 00 00','passager','IM','Étudiant(e) en IM à l\'IFRI.');
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_groups_user_id_group_id_b88eab82_uniq` (`user_id`,`group_id`),
  KEY `users_user_groups_group_id_9afc8d0e_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_user_groups_group_id_9afc8d0e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_user_groups_user_id_5f6f5a90_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_user_permissions_user_id_permission_id_43338c45_uniq` (`user_id`,`permission_id`),
  KEY `users_user_user_perm_permission_id_0b93982e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_user_user_perm_permission_id_0b93982e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_user_user_permissions_user_id_20aca447_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*M!999999\- enable the sandbox mode */ 
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

SET FOREIGN_KEY_CHECKS = 1;
