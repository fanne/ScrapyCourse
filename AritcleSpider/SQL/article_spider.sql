/*
Navicat MySQL Data Transfer

Source Server         : 10.163.46.92_own
Source Server Version : 50637
Source Host           : 10.163.46.92:3306
Source Database       : article_spider

Target Server Type    : MYSQL
Target Server Version : 50637
File Encoding         : 65001

Date: 2017-08-26 16:37:42
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for jobbole_article
-- ----------------------------
DROP TABLE IF EXISTS `jobbole_article`;
CREATE TABLE `jobbole_article` (
  `title` varchar(200) NOT NULL,
  `create_date` date DEFAULT NULL,
  `url` varchar(300) NOT NULL,
  `url_object_id` varchar(50) NOT NULL,
  `front_image_url` varchar(300) DEFAULT NULL,
  `front_image_path` varchar(200) DEFAULT NULL,
  `praise_nums` int(11) NOT NULL DEFAULT '0',
  `comment_nums` int(11) NOT NULL DEFAULT '0',
  `fav_nums` int(11) NOT NULL DEFAULT '0',
  `content` longtext,
  `tags` varchar(200) NOT NULL,
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of jobbole_article
-- ----------------------------
INSERT INTO `jobbole_article` VALUES ('cp 命令两个高效的用法', '2017-08-12', 'http://blog.jobbole.com/112170/', '0b8ff310585249119a5b31d70bda767d', null, null, '0', '0', '9', null, '');
INSERT INTO `jobbole_article` VALUES ('一文了解 Kubernetes 是什么？', '2017-08-23', 'http://blog.jobbole.com/112243/', '14cfc2026b582f161bc18bdb5bf704ab', null, null, '0', '0', '1', null, '');
INSERT INTO `jobbole_article` VALUES ('Nginx 缓存引发的跨域惨案', '2017-08-21', 'http://blog.jobbole.com/112224/', '1a6ec2a64adc4d7e67f112d418752843', null, null, '0', '0', '4', null, '');
INSERT INTO `jobbole_article` VALUES ('用神经网络训练一个文本分类器', '2017-08-10', 'http://blog.jobbole.com/112049/', '1b94069f855b02965e7341f1f26e4ce2', null, null, '0', '0', '4', null, '');
INSERT INTO `jobbole_article` VALUES ('Linux 包管理基础：apt、yum、dnf 和 pkg', '2017-08-20', 'http://blog.jobbole.com/112219/', '1e031f3dac72715c8de661ef03cc6ef1', null, null, '0', '0', '9', null, '');
INSERT INTO `jobbole_article` VALUES ('决策树算法及实现', '2017-08-16', 'http://blog.jobbole.com/112206/', '20f251db4302493feab2277f2e28cf93', null, null, '0', '0', '2', null, '');
INSERT INTO `jobbole_article` VALUES ('编写高质量代码的思考', '2017-08-10', 'http://blog.jobbole.com/112139/', '2b39c6050457697bdcf56fe2481a09cf', null, null, '0', '0', '2', null, '');
INSERT INTO `jobbole_article` VALUES ('Zookeeper，你可把我坑惨了！', '2017-08-22', 'http://blog.jobbole.com/112233/', '31a86b3ac18cd1f7d95efa9a354872a2', null, null, '0', '0', '1', null, '');
INSERT INTO `jobbole_article` VALUES ('如何做有效的Code Review？我有这些建议', '2017-08-15', 'http://blog.jobbole.com/112050/', '5eda13472020b0a94aa6bc350676f012', null, null, '0', '0', '3', null, '');
INSERT INTO `jobbole_article` VALUES ('程序员的自我修养：温故而知新', '2017-08-11', 'http://blog.jobbole.com/112161/', '697cda33f7258dcfabbacb139fb85b20', null, null, '0', '0', '3', null, '');
INSERT INTO `jobbole_article` VALUES ('CoreOS，一款 Linux 容器发行版', '2017-08-14', 'http://blog.jobbole.com/112189/', '6cbfecaa4a696000b1d800f677cb3f43', null, null, '0', '0', '0', null, '');
INSERT INTO `jobbole_article` VALUES ('提升 C++ 技能的 7 种方法', '2017-08-24', 'http://blog.jobbole.com/112246/', '7a050b13630b4c2a96626bde9331cd01', null, null, '0', '0', '1', null, '');
INSERT INTO `jobbole_article` VALUES ('6 个理由，为什么 GNOME 仍然是最好的 Linux 桌面环境', '2017-08-16', 'http://blog.jobbole.com/112167/', '85bd8601e0edbec62fafb940f1ad7501', null, null, '0', '0', '3', null, '');
INSERT INTO `jobbole_article` VALUES ('从分布式计算到分布式训练', '2017-08-21', 'http://blog.jobbole.com/112222/', '8ca27b6e450717e1a86cd115d118ba44', null, null, '0', '0', '3', null, '');
INSERT INTO `jobbole_article` VALUES ('PHP实现定时任务（非linux-shell方式，与操作系统无关）', '2017-08-16', 'http://blog.jobbole.com/112214/', '919eee6bab5d88995a4efb5f71a1e9de', null, null, '0', '0', '2', null, '');
INSERT INTO `jobbole_article` VALUES ('一个时代的结束：Solaris 系统的那些年，那些事', '2017-08-25', 'http://blog.jobbole.com/112268/', 'c2031fdb29548112c91025f9bbba3f1f', null, null, '0', '0', '0', null, '');
INSERT INTO `jobbole_article` VALUES ('150 多个 ML、NLP 和 Python 相关的教程', '2017-08-15', 'http://blog.jobbole.com/112185/', 'ce3a7725a878dcf107e5503031e8e276', null, null, '0', '0', '7', null, '');
INSERT INTO `jobbole_article` VALUES ('谷歌用两年时间研究了 180 个团队，发现高效团队有这五个特征', '2017-08-23', 'http://blog.jobbole.com/112239/', 'f82b2deb2e66636ba145fc06d7391f6f', null, null, '0', '0', '3', null, '');
INSERT INTO `jobbole_article` VALUES ('DevOps 团队之殇', '2017-08-23', 'http://blog.jobbole.com/112237/', 'fea447f655adc5e5a294480152ef9eb8', null, null, '0', '0', '1', null, '');
INSERT INTO `jobbole_article` VALUES ('最实用的 Linux 命令行使用技巧', '2017-08-24', 'http://blog.jobbole.com/112265/', 'ffadf132787e6e34490e266051346177', null, null, '0', '0', '1', null, '');
