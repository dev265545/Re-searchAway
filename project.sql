-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3307
-- Generation Time: Nov 28, 2022 at 05:13 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `project`
--

-- --------------------------------------------------------

--
-- Table structure for table `author`
--

CREATE TABLE `author` (
  `p_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `author`
--

INSERT INTO `author` (`p_id`, `user_id`) VALUES
(1010, 3),
(1011, 0),
(1012, 0),
(1013, 0),
(1014, 0),
(1015, 0);

-- --------------------------------------------------------

--
-- Table structure for table `liked_paper`
--

CREATE TABLE `liked_paper` (
  `liked_user_id` varchar(11) NOT NULL,
  `liked_p_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `liked_paper`
--

INSERT INTO `liked_paper` (`liked_user_id`, `liked_p_id`) VALUES
('dev406', 1012),
('dev406', 1013),
('dev406', 1014);

-- --------------------------------------------------------

--
-- Table structure for table `paper`
--

CREATE TABLE `paper` (
  `Title` text NOT NULL,
  `P_ID` int(11) NOT NULL,
  `Abstract` text NOT NULL,
  `Field_Of_research` varchar(200) NOT NULL,
  `Publisher_id` int(11) NOT NULL,
  `Date_of_Publish` date NOT NULL,
  `auth_id` varchar(11) NOT NULL,
  `likes` int(11) NOT NULL DEFAULT 0,
  `link` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `paper`
--

INSERT INTO `paper` (`Title`, `P_ID`, `Abstract`, `Field_Of_research`, `Publisher_id`, `Date_of_Publish`, `auth_id`, `likes`, `link`) VALUES
('A Survey of Physical Layer Security Techniques for 5G Wireless Networks and Challenges Ahead', 1012, 'Physical layer security which safeguards data\r\nconfidentiality based on the information-theoretic approaches\r\nhas received significant research interest recently. The key\r\nidea behind physical layer security is to utilize the intrinsic\r\nrandomness of the transmission channel to guarantee the\r\nsecurity in physical layer. The evolution toward 5G wireless\r\ncommunications poses new challenges for physical layer security\r\nresearch. This paper provides a latest survey of the physical\r\nlayer security research on various promising 5G technologies,\r\nincluding physical layer security coding, massive multiple-input\r\nmultiple-output, millimeter wave communications, heterogeneous\r\nnetworks, non-orthogonal multiple access, full duplex technology,\r\nand so on. Technical challenges which remain unresolved at\r\nthe time of writing are summarized and the future trends of\r\nphysical layer security in 5G and beyond are discussed.', ' Computer Networks, 5G, physical layer security, massive MMO, mmWave, heterogeneous network, NOMA, full duplex ', 1000, '2018-04-04', 'dev406', 2, ''),
('dd', 1013, 'dd', ' dd ', 1000, '2022-11-28', 'dev406', 1, ''),
('dec', 1014, 'f', ' ff ', 1005, '2022-11-25', 'dev406', 1, ''),
('A Survey of Physical Layer Security Techniques for 5G Wireless Networks and Challenges Ahead', 1015, 'Physical layer security which safeguards data confidentiality based on the information-theoretic approaches has received significant research interest recently. The key idea behind physical layer security is to utilize the intrinsic randomness of the transmission channel to guarantee the security in physical layer. The evolution toward 5G wireless communications poses new challenges for physical layer security research. This paper provides a latest survey of the physical layer security research on various promising 5G technologies, including physical layer security coding, massive multiple-input multiple-output, millimeter wave communications, heterogeneous networks, non-orthogonal multiple access, full duplex technology, and so on. Technical challenges which remain unresolved at the time of writing are summarized and the future trends of physical layer security in 5G and beyond are discussed.', ' Physical layer , Network security , 5G mobile communication , Encoding , Parity check codes , Wireless networks ', 1000, '2022-11-28', 'dev406', 0, 'https://ieeexplore.ieee.org/document/8335290');

--
-- Triggers `paper`
--
DELIMITER $$
CREATE TRIGGER `AUTH` AFTER INSERT ON `paper` FOR EACH ROW insert into author values(new.p_id, new.auth_id)
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `publisher`
--

CREATE TABLE `publisher` (
  `Pub_id` int(11) NOT NULL,
  `Name` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `publisher`
--

INSERT INTO `publisher` (`Pub_id`, `Name`) VALUES
(1000, 'IEEE'),
(1005, 'International Journal of Wireless Networks and Communications [IJWNC]'),
(1006, 'Journal of Computer Science and Application [JCSA]');

-- --------------------------------------------------------

--
-- Table structure for table `to_be_read`
--

CREATE TABLE `to_be_read` (
  `user_id_read` varchar(11) NOT NULL,
  `read_p_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `to_be_read`
--

INSERT INTO `to_be_read` (`user_id_read`, `read_p_id`) VALUES
('dev406', 1012);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` varchar(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `name`, `email`, `password`) VALUES
('dev406', 'Dev Gupta', 'guptadev406@gmail.com', 'pbkdf2:sha256:150000$H45cvvhb$592518d9c4ffbe7597b4968707371532f696711e4b677e13832d17510d78d86d');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `liked_paper`
--
ALTER TABLE `liked_paper`
  ADD PRIMARY KEY (`liked_user_id`,`liked_p_id`),
  ADD KEY `P_ID_fk` (`liked_p_id`);

--
-- Indexes for table `paper`
--
ALTER TABLE `paper`
  ADD PRIMARY KEY (`P_ID`);

--
-- Indexes for table `publisher`
--
ALTER TABLE `publisher`
  ADD PRIMARY KEY (`Pub_id`);

--
-- Indexes for table `to_be_read`
--
ALTER TABLE `to_be_read`
  ADD PRIMARY KEY (`user_id_read`,`read_p_id`),
  ADD KEY `P_ID_readfk` (`read_p_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `paper`
--
ALTER TABLE `paper`
  MODIFY `P_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1016;

--
-- AUTO_INCREMENT for table `publisher`
--
ALTER TABLE `publisher`
  MODIFY `Pub_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1007;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `liked_paper`
--
ALTER TABLE `liked_paper`
  ADD CONSTRAINT `P_ID_fk` FOREIGN KEY (`liked_p_id`) REFERENCES `paper` (`P_ID`),
  ADD CONSTRAINT `user_id_fk` FOREIGN KEY (`liked_user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `to_be_read`
--
ALTER TABLE `to_be_read`
  ADD CONSTRAINT `P_ID_readfk` FOREIGN KEY (`read_p_id`) REFERENCES `paper` (`P_ID`),
  ADD CONSTRAINT `user_id_readfk` FOREIGN KEY (`user_id_read`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
