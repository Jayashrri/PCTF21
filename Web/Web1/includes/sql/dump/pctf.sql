-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 28, 2020 at 05:11 AM
-- Server version: 8.0.22-0ubuntu0.20.04.3
-- PHP Version: 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pctf`
--

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `productid` int NOT NULL,
  `productname` varchar(255) NOT NULL,
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'No offers now :('
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`productid`, `productname`, `code`) VALUES
(7, 'Soap', 'hINuarZVYLszUHRqtBAC'),
(8, 'Toothpaste', 'I6toQZCwMzycFPjiWpL2'),
(9, 'Milk', 's1bDzuko6gNWRKhq4wZc'),
(10, 'Sugar', 'vzs7modPH6V0FEuXnbpI'),
(11, 'Bread', 'TLmSYGDVIdP7Rn6wbQji'),
(12, 'Ice Cream', 'u5Xq2c4C0iTlZ6V3GKAD'),
(13, 'lettuce', 'CGODjJsNnc9BTMYKUv4Z'),
(14, 'apples', 'AYIcBwE5PGhZlJigmvqn'),
(15, 'oranges', 'F0EcgLf7PA1yonZxC9jI'),
(16, 'peaches', 'S3R6XBHxPJNutgaDeUMr'),
(17, 'chicken', 'V73ljepQmkNfFcY4aWRu'),
(18, 'ketchup', 'Uk18pFVh6TuvNjziRtWA'),
(19, 'yogurt', 'q2XBGL7YZukvQw5jHDWi'),
(20, 'mayonnaise', 'nUKd3T8uhSXF1qyBvrJw'),
(21, 'mustard', 'Av8z7K6FqNxUj2ktweRQ'),
(22, 'toilet paper', 'pG2y8uHc1MxizCqETtgv'),
(23, 'dishwasher soap', 'LPYUvsEH90aIgA4rBOf6'),
(24, 'coffee', 'CcitMQ1YTDqFuLXw8E3y'),
(25, 'tea', 'OQsStrHVBAYPKwMZWkjy'),
(26, 'vinegar', 'Gbitux81BRlFUnCL3vyW'),
(27, 'flour', '21rhF7fNvCjUZeRAiDsl'),
(28, 'pepper', 'sNLYtJXxv1UGH0r63KCP'),
(29, 'cinnamon', 'TLrYXknC9ueEOmd4xay8'),
(30, 'batteries', 'qzNrT6o34AfyH0elk8xF'),
(31, 'hand lotion', 'VusHtjlGrIo07XpAQ5yC'),
(32, 'baby lotion', 'I7XBiaQoOrLPKkWREdM9'),
(33, 'chocolate milk', 'AxKYXR1GFJnBi3EQ4HCq'),
(34, 'pineapple', 'GgbheKHTVk9LB4oayRcD'),
(35, 'kiwi', 'pY4PuxtqW8iJyMH0hdSE'),
(36, 'strawberries', 'xWQs8LO6HETacbN21iDv'),
(37, 'cauliflower', 'DOfJnqEX57ihv2lG4s8A'),
(38, '', 'p_ctf{41w4y5_54n1t1z3_1nput}');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`) VALUES
(4, 'admin', '$2y$10$9RTCXrRT6dwkI43QqmlDSeI0WF6PwH87Q8r4c3dkjf.A5puen6DvO');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`productid`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `productid` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
