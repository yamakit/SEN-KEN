-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- ホスト: 127.0.0.1
-- 生成日時: 2021-06-11 08:38:14
-- サーバのバージョン： 10.4.17-MariaDB
-- PHP のバージョン: 8.0.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- データベース: `yolo_video_table`
--

-- --------------------------------------------------------

--
-- テーブルの構造 `yolo_video_table`
--

CREATE TABLE `yolo_video_table` (
  `video_id` int(11) NOT NULL,
  `frame1` int(11) NOT NULL,
  `frame2` int(11) NOT NULL,
  `ball_id` int(11) NOT NULL,
  `player_id` int(11) NOT NULL,
  `ans_id` int(11) NOT NULL,
  `x_coordinate` float NOT NULL,
  `y_coordinate` float NOT NULL,
  `video_path` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- テーブルのデータのダンプ `yolo_video_table`
--

INSERT INTO `yolo_video_table` (`video_id`, `frame1`, `frame2`, `ball_id`, `player_id`, `ans_id`, `x_coordinate`, `y_coordinate`, `video_path`) VALUES
(115, 1285, 1305, 1, 1, 1, 0.923642, 0.932166, './graphs\\ffmpeg_0212'),
(116, 1319, 1339, 1, 1, 1, 0.515218, 0.416855, './graphs\\ffmpeg_0213'),
(117, 1205, 1225, 1, 1, 1, 0.590841, 0.012521, './graphs\\ffmpeg_0214'),
(118, 1302, 1322, 1, 1, 1, 0.884127, 0.52203, './graphs\\ffmpeg_0215'),
(119, 1180, 1200, 1, 1, 1, 0.547837, 0.066614, './graphs\\ffmpeg_0217'),
(120, 1203, 1223, 1, 1, 1, 0.611232, 0.034754, './graphs\\ffmpeg_0218'),
(121, 0, 20, 1, 1, 1, 0.471505, 0.675853, './graphs\\ffmpeg_0219'),
(122, 1314, 1334, 1, 1, 1, 0.986259, 0.510076, './graphs\\ffmpeg_0220'),
(123, 1024, 1044, 1, 1, 1, 0.00222, 0.734172, './graphs\\ffmpeg_0222'),
(124, 1057, 1077, 1, 1, 1, 0.917505, 0.56345, './graphs\\ffmpeg_0224'),
(125, 987, 1007, 1, 1, 1, 0.568395, 0.00549, './graphs\\ffmpeg_0226'),
(126, 812, 832, 1, 1, 1, 0.539901, 0.620826, './graphs\\ffmpeg_0227'),
(127, 1251, 1271, 1, 1, 1, 0.630041, 0.436292, './graphs\\ffmpeg_0228'),
(128, 1190, 1210, 1, 1, 1, 0.909596, 0.593637, './graphs\\ffmpeg_0229'),
(129, 1253, 1273, 1, 1, 1, 0.897398, 0.586939, './graphs\\ffmpeg_0230'),
(130, 1302, 1322, 1, 1, 1, 0.904144, 0.626895, './graphs\\ffmpeg_0231'),
(131, 1272, 1292, 1, 1, 1, 0.940863, 0.593161, './graphs\\ffmpeg_0232'),
(132, 1108, 1128, 1, 1, 1, 0.670048, 0.610107, './graphs\\ffmpeg_0233'),
(133, 1233, 1253, 1, 1, 1, 0.451352, 0.991087, './graphs\\ffmpeg_0234'),
(134, 1256, 1276, 1, 1, 1, 0.620654, 0.641822, './graphs\\ffmpeg_0236'),
(135, 1219, 1239, 1, 1, 1, 0.413139, 0.893066, './graphs\\ffmpeg_0238'),
(136, 1142, 1162, 1, 1, 1, 0.764755, 0.757633, './graphs\\ffmpeg_0239'),
(137, 1243, 1263, 1, 1, 1, 0.790329, 0.677794, './graphs\\ffmpeg_0240'),
(138, 1302, 1322, 1, 1, 1, 0.703037, 0.505723, './graphs\\ffmpeg_0242'),
(139, 1278, 1298, 1, 1, 1, 0.966962, 0.728377, './graphs\\ffmpeg_0243'),
(140, 1104, 1124, 1, 1, 1, 0.579666, 0.184918, './graphs\\ffmpeg_0244'),
(141, 1300, 1320, 1, 1, 1, 0.81502, 0.928554, './graphs\\ffmpeg_0245'),
(142, 1225, 1245, 1, 1, 1, 0.891277, 0.711369, './graphs\\ffmpeg_0246'),
(143, 1359, 1379, 1, 1, 1, 0.819074, 0.754729, './graphs\\ffmpeg_0298'),
(144, 1188, 1208, 1, 1, 1, 0.398091, 0.48647, './graphs\\ffmpeg_0299'),
(145, 1281, 1301, 1, 1, 1, 0.0433127, 0.72089, './graphs\\ffmpeg_0302'),
(146, 1155, 1175, 1, 1, 1, 0.313382, 0.454904, './graphs\\ffmpeg_0303'),
(147, 1185, 1205, 1, 1, 1, 0.022539, 0.853633, './graphs\\ffmpeg_0304'),
(148, 1165, 1185, 1, 1, 1, 0.818726, 0.716557, './graphs\\ffmpeg_0308');

--
-- ダンプしたテーブルのインデックス
--

--
-- テーブルのインデックス `yolo_video_table`
--
ALTER TABLE `yolo_video_table`
  ADD UNIQUE KEY `id` (`video_id`) USING BTREE;

--
-- ダンプしたテーブルの AUTO_INCREMENT
--

--
-- テーブルの AUTO_INCREMENT `yolo_video_table`
--
ALTER TABLE `yolo_video_table`
  MODIFY `video_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=149;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
