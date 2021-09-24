-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- ホスト: 127.0.0.1
-- 生成日時: 2021-06-30 13:37:03
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
-- データベース: `sen-ken`
--

-- --------------------------------------------------------

--
-- テーブルの構造 `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `player_id` int(11) NOT NULL,
  `ball_id` int(11) NOT NULL,
  `name` varchar(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- テーブルのデータのダンプ `users`
--

INSERT INTO `users` (`id`, `player_id`, `ball_id`, `name`) VALUES
(1, 1, 1, '安西'),
(2, 2, 1, '花道'),
(3, 3, 1, '流川'),
(4, 4, 1, '仙道'),
(5, 5, 1, '板垣'),
(6, 6, 1, '横山'),
(7, 7, 1, '照本'),
(8, 8, 1, '迅'),
(9, 9, 1, '中川'),
(10, 10, 1, '山下'),
(11, 1, 2, 'あ'),
(12, 2, 2, 'い'),
(13, 3, 2, 'う'),
(14, 4, 2, 'え'),
(15, 5, 2, 'お'),
(16, 6, 2, 'か'),
(17, 7, 2, 'き'),
(18, 8, 2, 'く'),
(19, 9, 2, 'け'),
(20, 10, 2, 'こ'),
(21, 1, 3, 'さ'),
(22, 2, 3, 'し'),
(23, 3, 3, 'す'),
(24, 4, 3, 'せ'),
(25, 5, 3, 'そ'),
(26, 6, 3, 'た'),
(27, 7, 3, 'ち'),
(28, 8, 3, 'つ'),
(29, 9, 3, 'て'),
(30, 10, 3, 'と');

--
-- ダンプしたテーブルのインデックス
--

--
-- テーブルのインデックス `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- ダンプしたテーブルの AUTO_INCREMENT
--

--
-- テーブルの AUTO_INCREMENT `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
