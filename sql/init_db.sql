CREATE DATABASE flask_app;

USE flask_app;

CREATE TABLE user(
    uid INT AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL,
    email VARCHAR(320) NOT NULL,
    pwd VARCHAR(60) NOT NULL,
    is_manager BOOLEAN NOT NULL DEFAULT FALSE, /* DFT */
    created_at DATETIME NOT NULL DEFAULT NOW(), /* DFT */
    punished BOOLEAN NOT NULL DEFAULT FALSE, /* DFT */
    block_until DATETIME,
    expire_at DATETIME,
    PRIMARY KEY(uid),
    UNIQUE KEY(username, email)
);

CREATE TABLE userlog(
    idx INT AUTO_INCREMENT,
    uid INT NOT NULL,
    username VARCHAR(20) NOT NULL,
    email VARCHAR(320) NOT NULL,
    is_manager BOOLEAN NOT NULL,
    modified_at DATETIME NOT NULL DEFAULT NOW(), /* DFT */
    block_until DATETIME,
    expire_log_at DATETIME NOT NULL DEFAULT DATE_ADD(NOW(), INTERVAL 3 MONTH), /* DFT */
    mdtype VARCHAR(15) NOT NULL,
    PRIMARY KEY(idx)
);

CREATE TABLE punishlog(
    idx INT AUTO_INCREMENT,
    src_uid INT NOT NULL,
    tgt_id INT NOT NULL,
    punish_tgt_type VARCHAR(7) NOT NULL, /* ARTICLE, COMMENT, USER */
    logged_at DATETIME NOT NULL DEFAULT NOW(), /* DFT */
    expire_log_at DATETIME NOT NULL DEAFULT DATE_ADD(NOW(), INTERVAL 3 MONTH), /* DFT */
    PRIMARY KEY(idx)
);