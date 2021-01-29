-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: db:3306
-- Generation Time: Jan 29, 2021 at 07:38 PM
-- Server version: 8.0.22
-- PHP Version: 7.4.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pctfenc`
--

-- --------------------------------------------------------

--
-- Table structure for table `activation`
--

CREATE TABLE `activation` (
  `id` int NOT NULL,
  `code` varchar(255) NOT NULL,
  `used` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `activation`
--

INSERT INTO `activation` (`id`, `code`, `used`) VALUES
(2, 'A1ENERR4028HUIFDVBK', 0),
(3, '12UHDUFICVBUWEF9JUOBB', 0),
(4, 'SJKFGJK9OIQEFHO', 0),
(5, '9FGHJIOGS98FA9VU', 0),
(6, 'QUID39UFIVBUIOION', 0),
(7, '3JRBFLREG42UOVBJDCJ', 0),
(8, 'PRG90JIVOVISIHH', 0),
(9, 'VCIUF09VDFV890IFD', 0),
(10, 'MMDI3UHT94GBUOJUB', 0),
(11, 'CVXIGHUAOWF08GRH', 0),
(12, 'VRS9P8HTPIOAB9AVA9UB', 0),
(13, 'V9384BIUOBIPI', 0),
(14, '9BIPAVIBU8T8G97G', 0),
(15, '8PVBIURWAJVBUI7G', 0),
(16, 'IUB8G7VBIUAWWBUI', 0),
(17, 'ZVSIOSHVV94TUVHU', 0),
(18, 'V4WAONAYFO9YERB', 0);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `isPremium` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `isPremium`) VALUES
(6, 'root', '$2y$10$2afH7RKKXA5hbl8LGFv.V.k78jvP7qwK7xyE46MODcJXdb..Vc2gm', 0),
(7, 'sudo', '$2y$10$X2YX168OVl/15bjahvFST.qf6pAEw5DnagniGMpyAoQ7D5eM1K7Oe', 0),
(8, 'admin', '$2y$10$/84W4uK4zFhPMQavFL3pceHdSRnhC5HhTWvt.6adwXJUaR9yHBF2G', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `activation`
--
ALTER TABLE `activation`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `activation`
--
ALTER TABLE `activation`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
