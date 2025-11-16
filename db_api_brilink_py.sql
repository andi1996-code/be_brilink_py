-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 05, 2025 at 10:35 AM
-- Server version: 8.0.30
-- PHP Version: 8.3.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_api_brilink_py`
--

-- --------------------------------------------------------

--
-- Table structure for table `agent_profiles`
--

CREATE TABLE `agent_profiles` (
  `id` bigint UNSIGNED NOT NULL,
  `user_id` bigint UNSIGNED NOT NULL,
  `owner_id` bigint UNSIGNED DEFAULT NULL,
  `agent_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `total_balance` decimal(15,2) NOT NULL DEFAULT '0.00',
  `logo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `agent_profiles`
--

INSERT INTO `agent_profiles` (`id`, `user_id`, `owner_id`, `agent_name`, `address`, `phone`, `total_balance`, `logo`, `created_at`, `updated_at`) VALUES
(1, 2, 2, 'Brilink Pusat Updated', 'Jl. Sudirman No. 10', '082345678901', 0.00, 'https://example.com/logo.png', '2025-10-28 23:34:11', '2025-10-29 05:04:19'),
(2, 3, 3, 'Jane Owner Agent', NULL, NULL, 0.00, NULL, '2025-10-29 03:06:40', '2025-10-29 03:06:40');

-- --------------------------------------------------------

--
-- Table structure for table `bank_fees`
--

CREATE TABLE `bank_fees` (
  `id` bigint UNSIGNED NOT NULL,
  `edc_machine_id` bigint UNSIGNED NOT NULL,
  `service_id` bigint UNSIGNED NOT NULL,
  `fee` decimal(15,2) NOT NULL DEFAULT '0.00',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `bank_fees`
--

INSERT INTO `bank_fees` (`id`, `edc_machine_id`, `service_id`, `fee`, `created_at`, `updated_at`) VALUES
(2, 5, 9, 2500.00, '2025-10-30 02:44:53', '2025-10-30 02:44:53');

-- --------------------------------------------------------

--
-- Table structure for table `cash_flows`
--

CREATE TABLE `cash_flows` (
  `id` bigint UNSIGNED NOT NULL,
  `agent_profile_id` bigint UNSIGNED DEFAULT NULL,
  `user_id` bigint UNSIGNED NOT NULL,
  `type` enum('cash_in','cash_out') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` decimal(15,2) NOT NULL DEFAULT '0.00',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `cash_flows`
--

INSERT INTO `cash_flows` (`id`, `agent_profile_id`, `user_id`, `type`, `source`, `amount`, `description`, `created_at`, `updated_at`) VALUES
(4, 2, 3, 'cash_in', 'Penarikan ATM', 807583.00, 'Pemasukan darurat - Juni 2024', '2025-10-22 14:53:12', '2025-10-29 08:22:20'),
(5, 2, 3, 'cash_out', 'Penarikan Pemilik', 490910.00, 'Pengeluaran darurat - Agustus 2024', '2025-09-29 02:44:09', '2025-10-29 08:22:20'),
(6, 1, 2, 'cash_in', 'Penjualan Token Listrik', 1887181.00, 'Pemasukan terjadwal - Mei 2025', '2025-10-10 09:13:38', '2025-10-29 08:22:20'),
(7, 1, 2, 'cash_in', 'Setoran dari Pemilik', 500000.00, 'Setoran modal awal', '2025-10-30 00:18:32', '2025-10-30 00:18:32'),
(8, 1, 2, 'cash_out', 'Penarikan Pemilik', 100000.00, 'Penarikan keuntungan', '2025-10-30 00:24:37', '2025-10-30 00:24:37'),
(9, 1, 2, 'cash_out', 'Modal awal', 25000.00, 'beli nasi padang', '2025-10-30 00:25:57', '2025-10-30 00:25:57');

-- --------------------------------------------------------

--
-- Table structure for table `edc_machines`
--

CREATE TABLE `edc_machines` (
  `id` bigint UNSIGNED NOT NULL,
  `agent_profile_id` bigint UNSIGNED DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `bank_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `account_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `saldo` decimal(15,2) NOT NULL DEFAULT '0.00',
  `status` enum('active','inactive') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `edc_machines`
--

INSERT INTO `edc_machines` (`id`, `agent_profile_id`, `name`, `bank_name`, `account_number`, `saldo`, `status`, `created_at`, `updated_at`) VALUES
(4, 1, 'EDC BCA 002', 'BCA', '0987654321', 100000.00, 'active', '2025-10-29 05:04:57', '2025-10-29 08:23:52'),
(5, 1, 'EDC BNI', 'BNI', '1234567890', 5000000.00, 'active', '2025-10-29 08:31:42', '2025-10-29 08:31:42');

-- --------------------------------------------------------

--
-- Table structure for table `receipt_templates`
--

CREATE TABLE `receipt_templates` (
  `id` bigint UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `agent_profile_id` bigint UNSIGNED DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Default Template',
  `html_template` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `css` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `is_default` tinyint(1) NOT NULL DEFAULT '0',
  `version` int NOT NULL DEFAULT '1',
  `paper_size` enum('58mm','80mm','88mm') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '80mm',
  `created_by` bigint UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `requires_target` tinyint(1) NOT NULL DEFAULT '0',
  `category` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`id`, `name`, `requires_target`, `category`, `description`, `created_at`, `updated_at`) VALUES
(9, 'Transfer', 1, 'Transfer', '-', '2025-10-28 23:06:44', '2025-10-28 23:12:51'),
(10, 'Tarik Tunai', 0, 'Tarik Tunai', '-', '2025-10-28 23:09:12', '2025-10-28 23:09:12');

-- --------------------------------------------------------

--
-- Table structure for table `service_fees`
--

CREATE TABLE `service_fees` (
  `id` bigint UNSIGNED NOT NULL,
  `service_id` bigint UNSIGNED NOT NULL,
  `min_amount` decimal(15,2) NOT NULL DEFAULT '0.00',
  `max_amount` decimal(15,2) NOT NULL DEFAULT '0.00',
  `fee` decimal(15,2) NOT NULL DEFAULT '0.00',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `service_fees`
--

INSERT INTO `service_fees` (`id`, `service_id`, `min_amount`, `max_amount`, `fee`, `created_at`, `updated_at`) VALUES
(1, 9, 1.00, 100000.00, 5000.00, '2025-10-28 23:44:06', '2025-10-28 23:44:06'),
(2, 9, 101000.00, 1000000.00, 7000.00, '2025-10-28 23:44:40', '2025-10-28 23:44:40'),
(3, 10, 100000.00, 1000000.00, 7000.00, '2025-10-28 23:45:06', '2025-10-28 23:45:06');

-- --------------------------------------------------------

--
-- Table structure for table `token_blacklist`
--

CREATE TABLE `token_blacklist` (
  `id` bigint NOT NULL,
  `token` varchar(500) NOT NULL,
  `user_id` bigint NOT NULL,
  `blacklisted_at` datetime DEFAULT NULL,
  `expires_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `token_blacklist`
--

INSERT INTO `token_blacklist` (`id`, `token`, `user_id`, `blacklisted_at`, `expires_at`) VALUES
(1, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJlbWFpbCI6ImpvaG5AZXhhbXBsZS5jb20iLCJpYXQiOjE3NjE4MDc0NjYsImV4cCI6MTc2MTg5Mzg2Nn0._bmhf-1md4mutF96bfZObfzlNMSiwYxoavvWGtz1j3I', 2, '2025-10-30 07:03:21', '2025-10-31 13:57:46');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` bigint UNSIGNED NOT NULL,
  `transaction_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `edc_machine_id` bigint UNSIGNED NOT NULL,
  `service_id` bigint UNSIGNED NOT NULL,
  `agent_profile_id` bigint UNSIGNED NOT NULL,
  `user_id` bigint UNSIGNED NOT NULL,
  `customer_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `target_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `reference_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `amount` decimal(15,2) NOT NULL DEFAULT '0.00',
  `service_fee` decimal(15,2) NOT NULL DEFAULT '0.00',
  `bank_fee` decimal(15,2) NOT NULL DEFAULT '0.00',
  `extra_fee` decimal(15,2) NOT NULL DEFAULT '0.00',
  `net_profit` decimal(15,2) NOT NULL DEFAULT '0.00',
  `payment_method` enum('cash','edc','other') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'cash',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `transaction_number`, `edc_machine_id`, `service_id`, `agent_profile_id`, `user_id`, `customer_name`, `target_number`, `reference_number`, `amount`, `service_fee`, `bank_fee`, `extra_fee`, `net_profit`, `payment_method`, `created_at`, `updated_at`) VALUES
(22, 'TXN202510292222072512', 4, 10, 1, 4, 'Ani Suryani', NULL, 'REF463593', 201553.00, 7000.00, 0.00, 0.00, 201553.00, 'cash', '2025-10-12 06:46:29', '2025-10-29 08:22:07'),
(23, 'TXN202510292222073068', 4, 9, 1, 4, 'Dedi Kusuma', '086136289973', 'REF418869', 1159104.00, 0.00, 0.00, 0.00, 1159104.00, 'cash', '2025-10-15 03:11:47', '2025-10-29 08:22:07'),
(24, 'TXN202510292222075530', 4, 9, 1, 4, 'Dewi Lestari', '089463445510', 'REF847953', 1240245.00, 0.00, 0.00, 0.00, 1240245.00, 'cash', '2025-10-07 15:34:51', '2025-10-29 08:22:07'),
(25, 'TXN202510292222072949', 4, 9, 1, 4, 'Budi Santoso', '082054700156', 'REF354764', 1682039.00, 0.00, 0.00, 0.00, 1682039.00, 'cash', '2025-10-19 09:49:48', '2025-10-29 08:22:07'),
(26, 'TXN202510292222077706', 4, 9, 2, 4, 'Budi Santoso', '084951635998', 'REF109556', 1442584.00, 0.00, 0.00, 0.00, 1442584.00, 'cash', '2025-10-18 11:29:31', '2025-10-29 08:22:07'),
(27, 'TXN202510292234569085', 4, 10, 1, 4, 'Maya Sari', NULL, 'REF440425', 232940.00, 7000.00, 0.00, 0.00, 232940.00, 'cash', '2025-10-29 07:14:50', '2025-10-29 08:34:56'),
(28, 'TXN202510292234561019', 5, 9, 1, 4, 'Siti Aminah', '081447553648', 'REF504448', 1212715.00, 0.00, 0.00, 0.00, 1212715.00, 'cash', '2025-10-29 06:13:09', '2025-10-29 08:34:56'),
(29, 'TXN202510292234567226', 5, 9, 2, 4, 'Dewi Lestari', '088603568604', 'REF757459', 476202.00, 7000.00, 0.00, 3835.00, 472367.00, 'cash', '2025-10-29 11:15:54', '2025-10-29 08:34:56'),
(30, 'TXN202510292234563650', 5, 9, 1, 4, 'Hendra Gunawan', '083373041555', 'REF641180', 843606.00, 7000.00, 0.00, 0.00, 843606.00, 'cash', '2025-10-29 05:27:02', '2025-10-29 08:34:56'),
(31, 'TXN202510292234561782', 4, 9, 2, 4, 'Sri Wahyuni', '081526618889', 'REF261078', 777989.00, 7000.00, 0.00, 0.00, 777989.00, 'cash', '2025-10-29 11:20:06', '2025-10-29 08:34:56');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` enum('owner','kasir') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'owner',
  `agent_profile_id` bigint UNSIGNED DEFAULT NULL,
  `status` enum('active','inactive') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'active',
  `remember_token` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `role`, `agent_profile_id`, `status`, `remember_token`, `created_at`, `updated_at`) VALUES
(2, 'John Doe', 'john@example.com', 'pbkdf2:sha256:600000$nGcJTfjmujx2Vzft$06b99232bcc302f9ab889496f21a8e2a3e2a2d79f32792c46e8b8de5ad3a0d87', 'owner', NULL, 'active', NULL, '2025-10-28 08:45:33', '2025-10-28 08:45:33'),
(3, 'Jane Owner', 'jane@example.com', 'pbkdf2:sha256:600000$tgY6ktcJa4P7zqEg$073f76ed406bbf1ec179eb68975d3bf3902f08da7389e33dd639dd95b7e418e7', 'owner', 2, 'active', NULL, '2025-10-29 03:06:40', '2025-10-29 03:06:40'),
(4, 'Bob Kasir', 'bob@example.com', 'pbkdf2:sha256:600000$YQMuZoZGQ9wbtQO8$2dddfcbc9fbcc8774e30f989cfb22f177fe2f853aca3c7463bc44ca35a16967c', 'kasir', 2, 'active', NULL, '2025-10-29 03:06:56', '2025-10-29 03:06:56');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `agent_profiles`
--
ALTER TABLE `agent_profiles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `agent_profiles_user_id_foreign` (`user_id`),
  ADD KEY `fk_agent_owner` (`owner_id`);

--
-- Indexes for table `bank_fees`
--
ALTER TABLE `bank_fees`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bank_fees_edc_machine_id_foreign` (`edc_machine_id`),
  ADD KEY `bank_fees_service_id_foreign` (`service_id`);

--
-- Indexes for table `cash_flows`
--
ALTER TABLE `cash_flows`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cash_flows_user_id_foreign` (`user_id`),
  ADD KEY `fk_cash_agent` (`agent_profile_id`);

--
-- Indexes for table `edc_machines`
--
ALTER TABLE `edc_machines`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_edc_agent` (`agent_profile_id`);

--
-- Indexes for table `receipt_templates`
--
ALTER TABLE `receipt_templates`
  ADD PRIMARY KEY (`id`),
  ADD KEY `receipt_templates_agent_profile_id_foreign` (`agent_profile_id`),
  ADD KEY `receipt_templates_created_by_foreign` (`created_by`);

--
-- Indexes for table `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `service_fees`
--
ALTER TABLE `service_fees`
  ADD PRIMARY KEY (`id`),
  ADD KEY `service_fees_service_id_foreign` (`service_id`);

--
-- Indexes for table `token_blacklist`
--
ALTER TABLE `token_blacklist`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `token` (`token`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `transactions_transaction_number_unique` (`transaction_number`),
  ADD KEY `transactions_edc_machine_id_foreign` (`edc_machine_id`),
  ADD KEY `transactions_service_id_foreign` (`service_id`),
  ADD KEY `transactions_user_id_foreign` (`user_id`),
  ADD KEY `fk_transactions_agent` (`agent_profile_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_email_unique` (`email`),
  ADD KEY `fk_user_agent` (`agent_profile_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `agent_profiles`
--
ALTER TABLE `agent_profiles`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `bank_fees`
--
ALTER TABLE `bank_fees`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `cash_flows`
--
ALTER TABLE `cash_flows`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `edc_machines`
--
ALTER TABLE `edc_machines`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `receipt_templates`
--
ALTER TABLE `receipt_templates`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `services`
--
ALTER TABLE `services`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `service_fees`
--
ALTER TABLE `service_fees`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `token_blacklist`
--
ALTER TABLE `token_blacklist`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `agent_profiles`
--
ALTER TABLE `agent_profiles`
  ADD CONSTRAINT `agent_profiles_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_agent_owner` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `bank_fees`
--
ALTER TABLE `bank_fees`
  ADD CONSTRAINT `bank_fees_edc_machine_id_foreign` FOREIGN KEY (`edc_machine_id`) REFERENCES `edc_machines` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `bank_fees_service_id_foreign` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `cash_flows`
--
ALTER TABLE `cash_flows`
  ADD CONSTRAINT `cash_flows_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_cash_agent` FOREIGN KEY (`agent_profile_id`) REFERENCES `agent_profiles` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `edc_machines`
--
ALTER TABLE `edc_machines`
  ADD CONSTRAINT `fk_edc_agent` FOREIGN KEY (`agent_profile_id`) REFERENCES `agent_profiles` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `receipt_templates`
--
ALTER TABLE `receipt_templates`
  ADD CONSTRAINT `receipt_templates_agent_profile_id_foreign` FOREIGN KEY (`agent_profile_id`) REFERENCES `agent_profiles` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `receipt_templates_created_by_foreign` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `service_fees`
--
ALTER TABLE `service_fees`
  ADD CONSTRAINT `service_fees_service_id_foreign` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `fk_transactions_agent` FOREIGN KEY (`agent_profile_id`) REFERENCES `agent_profiles` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `transactions_edc_machine_id_foreign` FOREIGN KEY (`edc_machine_id`) REFERENCES `edc_machines` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `transactions_service_id_foreign` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `transactions_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `fk_user_agent` FOREIGN KEY (`agent_profile_id`) REFERENCES `agent_profiles` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
