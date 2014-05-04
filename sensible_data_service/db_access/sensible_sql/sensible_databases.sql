CREATE DATABASE IF NOT EXISTS dk_dtu_compute_facebook;
USE dk_dtu_compute_facebook;

CREATE TABLE IF NOT EXISTS main (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(40) not null,
    facebook_id VARCHAR(40),
    data LONGBLOB,
    data_type VARCHAR(20),
    PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(40) not null,
    facebook_id VARCHAR(40),
    data LONGBLOB,
    data_type VARCHAR(20),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(40) not null,
    facebook_id VARCHAR(40),
    data LONGBLOB,
    data_type VARCHAR(20),
    PRIMARY KEY (id)
);


CREATE DATABASE IF NOT EXISTS edu_mit_media_funf_probe_builtin_BluetoothProbe;
USE edu_mit_media_funf_probe_builtin_BluetoothProbe;

CREATE TABLE IF NOT EXISTS main (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    class INT,
    bt_mac VARCHAR(64),
    name TEXT,
    rssi INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (bt_mac, timestamp, user)

);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    class INT,
    bt_mac VARCHAR(64),
    name TEXT,
    rssi INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (bt_mac, timestamp, user)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    class INT,
    bt_mac VARCHAR(64),
    name TEXT,
    rssi INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (bt_mac, timestamp, user)
);


CREATE DATABASE IF NOT EXISTS edu_mit_media_funf_probe_builtin_CallLogProbe;
USE edu_mit_media_funf_probe_builtin_CallLogProbe;

CREATE TABLE IF NOT EXISTS main (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    duration INT,
    name TEXT,
    number VARCHAR(40),
    numbertype VARCHAR(40),
    type INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (number, type, timestamp, user)

);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    duration INT,
    name TEXT,
    number VARCHAR(40),
    numbertype VARCHAR(40),
    type INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (number, type, timestamp, user)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    duration INT,
    name TEXT,
    number VARCHAR(40),
    numbertype VARCHAR(40),
    type INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (number, type, timestamp, user)
);

CREATE DATABASE IF NOT EXISTS edu_mit_media_funf_probe_builtin_CellProbe;
USE edu_mit_media_funf_probe_builtin_CellProbe;

CREATE TABLE IF NOT EXISTS main (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    cid INT,
    lac INT,
    psc INT,
    type INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (cid, lac, psc, type, timestamp, user)

);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    cid INT,
    lac INT,
    psc INT,
    type INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (cid, lac, psc, type, timestamp, user)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    cid INT,
    lac INT,
    psc INT,
    type INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (cid, lac, psc, type, timestamp, user)
);

CREATE DATABASE IF NOT EXISTS edu_mit_media_funf_probe_builtin_ContactProbe;
USE edu_mit_media_funf_probe_builtin_ContactProbe;

CREATE TABLE IF NOT EXISTS main (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    contact_id INT,
    display_name VARCHAR(40),
    last_time_contacted INT,
    lookup VARCHAR(40),
    starred INT,
    times_contacted INT,
    _id INT,
    data1 TEXT,
    data2 TEXT,
    data3 TEXT,
    data4 TEXT,
    mimetype VARCHAR(60),
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (mimetype, contact_id, timestamp, user)

);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    contact_id INT,
    display_name VARCHAR(40),
    last_time_contacted INT,
    lookup VARCHAR(40),
    starred INT,
    times_contacted INT,
    _id INT,
    data1 TEXT,
    data2 TEXT,
    data3 TEXT,
    data4 TEXT,
    mimetype VARCHAR(60),
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (mimetype, contact_id, timestamp, user)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    contact_id INT,
    display_name VARCHAR(40),
    last_time_contacted INT,
    lookup VARCHAR(40),
    starred INT,
    times_contacted INT,
    _id INT,
    data1 TEXT,
    data2 TEXT,
    data3 TEXT,
    data4 TEXT,
    mimetype VARCHAR(60),
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (mimetype, contact_id, timestamp, user)
);



CREATE DATABASE IF NOT EXISTS edu_mit_media_funf_probe_builtin_HardwareInfoProbe;
USE edu_mit_media_funf_probe_builtin_HardwareInfoProbe;

CREATE TABLE IF NOT EXISTS main (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    android_id VARCHAR(64),
    bt_mac VARCHAR(64),
    brand VARCHAR(64),
    model VARCHAR(64),
    wifi_mac VARCHAR(64),
    device VARCHAR(64),
    device_bt_mac VARCHAR(64),
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (android_id, timestamp, user)

);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    android_id VARCHAR(64),
    bt_mac VARCHAR(64),
    brand VARCHAR(64),
    model VARCHAR(64),
    wifi_mac VARCHAR(64),
    device VARCHAR(64),
    device_bt_mac VARCHAR(64),
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (android_id, timestamp, user)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    android_id VARCHAR(64),
    bt_mac VARCHAR(64),
    brand VARCHAR(64),
    model VARCHAR(64),
    wifi_mac VARCHAR(64),
    device VARCHAR(64),
    device_bt_mac VARCHAR(64),
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (android_id, timestamp, user)
);



CREATE DATABASE IF NOT EXISTS edu_mit_media_funf_probe_builtin_LocationProbe;
USE edu_mit_media_funf_probe_builtin_LocationProbe;

CREATE TABLE IF NOT EXISTS main (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    lat DOUBLE,
    lon DOUBLE,
    accuracy DOUBLE,
    provider VARCHAR(20),
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (lat, lon, provider, timestamp, user)

);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    lat DOUBLE,
    lon DOUBLE,
    accuracy DOUBLE,
    provider VARCHAR(20),
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (lat, lon, provider, timestamp, user)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    lat DOUBLE,
    lon DOUBLE,
    accuracy DOUBLE,
    provider VARCHAR(20),
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (lat, lon, provider, timestamp, user)
);



CREATE DATABASE IF NOT EXISTS edu_mit_media_funf_probe_builtin_ScreenProbe;
USE edu_mit_media_funf_probe_builtin_ScreenProbe;

CREATE TABLE IF NOT EXISTS main (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    screen_on TINYINT(1),
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (screen_on, timestamp, user)

);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    screen_on TINYINT(1),
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (screen_on, timestamp, user)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    screen_on TINYINT(1),
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (screen_on, timestamp, user)
);



CREATE DATABASE IF NOT EXISTS edu_mit_media_funf_probe_builtin_SMSProbe;
USE edu_mit_media_funf_probe_builtin_SMSProbe;

CREATE TABLE IF NOT EXISTS main (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    address VARCHAR(40),
    body VARCHAR(40),
    person VARCHAR(40),
    protocol INT,
    message_read TINYINT(1),
    service_center VARCHAR(40),
    status INT,
    subject VARCHAR(40),
    thread_id INT,
    type INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (type, body, address, timestamp, user)

);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    address VARCHAR(40),
    body VARCHAR(40),
    person VARCHAR(40),
    protocol INT,
    message_read TINYINT(1),
    service_center VARCHAR(40),
    status INT,
    subject VARCHAR(40),
    thread_id INT,
    type INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (type, body, address, timestamp, user)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    address VARCHAR(40),
    body VARCHAR(40),
    person VARCHAR(40),
    protocol INT,
    message_read TINYINT(1),
    service_center VARCHAR(40),
    status INT,
    subject VARCHAR(40),
    thread_id INT,
    type INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (type, body, address, timestamp, user)
);



CREATE DATABASE IF NOT EXISTS edu_mit_media_funf_probe_builtin_TimeOffsetProbe;
USE edu_mit_media_funf_probe_builtin_TimeOffsetProbe;

CREATE TABLE IF NOT EXISTS main (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    time_offset FLOAT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (time_offset, timestamp, user)

);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    time_offset FLOAT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (time_offset, timestamp, user)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    time_offset FLOAT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (time_offset, timestamp, user)
);



CREATE DATABASE IF NOT EXISTS edu_mit_media_funf_probe_builtin_WifiProbe;
USE edu_mit_media_funf_probe_builtin_WifiProbe;

CREATE TABLE IF NOT EXISTS main (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    bssid VARCHAR(40),
    ssid VARCHAR(64),
    level INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (bssid, level, timestamp, user)

);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    bssid VARCHAR(40),
    ssid VARCHAR(64),
    level INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (bssid, level, timestamp, user)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    bssid VARCHAR(40),
    ssid VARCHAR(64),
    level INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (bssid, level, timestamp, user)
);



CREATE DATABASE IF NOT EXISTS dk_dtu_compute_questionnaire;
USE dk_dtu_compute_questionnaire;

CREATE TABLE IF NOT EXISTS main (
    id INT NOT NULL AUTO_INCREMENT,
    form_version VARCHAR(40),
    human_readable_question TEXT,
    human_readable_response TEXT,
    timestamp DATETIME,
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    response VARCHAR(300),
    variable_name VARCHAR(40),
    user VARCHAR(40) not null,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (form_version, response, variable_name, user)

);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    form_version VARCHAR(40),
    human_readable_question TEXT,
    human_readable_response TEXT,
    timestamp DATETIME,
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    response VARCHAR(300),
    variable_name VARCHAR(40),
    user VARCHAR(40) not null,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (form_version, response, variable_name, user)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    form_version VARCHAR(40),
    human_readable_question TEXT,
    human_readable_response TEXT,
    timestamp DATETIME,
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    response VARCHAR(300),
    variable_name VARCHAR(40),
    user VARCHAR(40) not null,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (form_version, response, variable_name, user)
);

CREATE DATABASE IF NOT EXISTS dk_dtu_compute_experience_sampling;
USE dk_dtu_compute_experience_sampling;

CREATE TABLE IF NOT EXISTS main (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    answer LONGBLOB,
    answer_type VARCHAR(20),
    question_type VARCHAR(20)
    uniqueness_hash BINARY(20),
    PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    answer LONGBLOB,
    answer_type VARCHAR(20),
    question_type VARCHAR(20)
    uniqueness_hash BINARY(20),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(64),
    timestamp_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user VARCHAR(64) not null,
    uuid VARCHAR(64),
    answer LONGBLOB,
    answer_type VARCHAR(20),
    question_type VARCHAR(20),
    uniqueness_hash BINARY(20),
    PRIMARY KEY (id)
);
