CREATE DATABASE IF NOT EXISTS facebook;
USE facebook;

CREATE TABLE IF NOT EXISTS main (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    user VARCHAR(40),
    facebook_id VARCHAR(40),
    data LONGBLOB,
    data_type VARCHAR(20),
    PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    user VARCHAR(40),
    facebook_id VARCHAR(40),
    data LONGBLOB,
    data_type VARCHAR(20),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    user VARCHAR(40),
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
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    class INT,
    bt_mac VARCHAR(40) not null,
    name VARCHAR(40),
    rssi INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (bt_mac, timestamp, user)

);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    class INT,
    bt_mac VARCHAR(40) not null,
    name VARCHAR(40),
    rssi INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (bt_mac, timestamp, user)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    class INT,
    bt_mac VARCHAR(40) not null,
    name VARCHAR(40),
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
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    duration INT,
    name VARCHAR(40),
    number VARCHAR(40),
    number_type VARCHAR(40),
    type INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (number, type, timestamp, user)

);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    duration INT,
    name VARCHAR(40),
    number VARCHAR(40),
    number_type VARCHAR(40),
    type INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (number, type, timestamp, user)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    duration INT,
    name VARCHAR(40),
    number VARCHAR(40),
    number_type VARCHAR(40),
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
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
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
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
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
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
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
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    contact_id INT,
    display_name VARCHAR(40),
    last_time_contacted INT,
    lookup VARCHAR(40),
    starred INT,
    times_contacted INT,
    _id INT,
    data1 INT,
    data2 INT,
    data3 INT,
    data4 INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (display_name, timestamp, user)

);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    contact_id INT,
    display_name VARCHAR(40),
    last_time_contacted INT,
    lookup VARCHAR(40),
    starred INT,
    times_contacted INT,
    _id INT,
    data1 INT,
    data2 INT,
    data3 INT,
    data4 INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (display_name, timestamp, user)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    contact_id INT,
    display_name VARCHAR(40),
    last_time_contacted INT,
    lookup VARCHAR(40),
    starred INT,
    times_contacted INT,
    _id INT,
    data1 INT,
    data2 INT,
    data3 INT,
    data4 INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (display_name, timestamp, user)
);



CREATE DATABASE IF NOT EXISTS edu_mit_media_funf_probe_builtin_HardwareInfoProbe;
USE edu_mit_media_funf_probe_builtin_HardwareInfoProbe;

CREATE TABLE IF NOT EXISTS main (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    android_id VARCHAR(40),
    bt_mac VARCHAR(40),
    brand VARCHAR(20),
    model VARCHAR(20),
    wifi_mac VARCHAR(40),
    device VARCHAR(40),
    device_bt_mac VARCHAR(20),
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (android_id, timestamp, user)

);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    android_id VARCHAR(40),
    bt_mac VARCHAR(40),
    brand VARCHAR(20),
    model VARCHAR(20),
    wifi_mac VARCHAR(40),
    device VARCHAR(40),
    device_bt_mac VARCHAR(20),
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (android_id, timestamp, user)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    android_id VARCHAR(40),
    bt_mac VARCHAR(40),
    brand VARCHAR(20),
    model VARCHAR(20),
    wifi_mac VARCHAR(40),
    device VARCHAR(40),
    device_bt_mac VARCHAR(20),
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (android_id, timestamp, user)
);



CREATE DATABASE IF NOT EXISTS edu_mit_media_funf_probe_builtin_LocationProbe;
USE edu_mit_media_funf_probe_builtin_LocationProbe;

CREATE TABLE IF NOT EXISTS main (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
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
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
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
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
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
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    screen_on TINYINT(1),
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (screen_on, timestamp, user)

);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    screen_on TINYINT(1),
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (screen_on, timestamp, user)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
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
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    address VARCHAR(40),
    body VARCHAR(40),
    person VARCHAR(40),
    protocol INT,
    message_read TINYINT(1),
    service_center INT,
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
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    address VARCHAR(40),
    body VARCHAR(40),
    person VARCHAR(40),
    protocol INT,
    message_read TINYINT(1),
    service_center INT,
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
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    address VARCHAR(40),
    body VARCHAR(40),
    person VARCHAR(40),
    protocol INT,
    message_read TINYINT(1),
    service_center INT,
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
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    time_offset INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (time_offset, timestamp, user)

);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    time_offset INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (time_offset, timestamp, user)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    time_offset INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (time_offset, timestamp, user)
);



CREATE DATABASE IF NOT EXISTS edu_mit_media_funf_probe_builtin_WifiProbe;
USE edu_mit_media_funf_probe_builtin_WifiProbe;

CREATE TABLE IF NOT EXISTS main (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    bssid VARCHAR(40),
    ssid VARCHAR(40),
    level INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (bssid, timestamp, user)

);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    bssid VARCHAR(40),
    ssid VARCHAR(40),
    level INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (bssid, timestamp, user)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME,
    device_id VARCHAR(40),
    sensible_token VARCHAR(20),
    timestamp_added DATETIME not null,
    user VARCHAR(40) not null,
    uuid VARCHAR(40),
    bssid VARCHAR(40),
    ssid VARCHAR(40),
    level INT,
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (bssid, timestamp, user)
);



CREATE DATABASE IF NOT EXISTS questionnaire;
USE questionnaire;

CREATE TABLE IF NOT EXISTS main (
    id INT NOT NULL AUTO_INCREMENT,
    form_version VARCHAR(40),
    human_readable_question TEXT,
    human_readable_response TEXT,
    last_answered DATETIME,
    response VARCHAR(120),
    variable_name VARCHAR(40),
    user VARCHAR(40),
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (form_version, response, variable_name, user)

);
CREATE TABLE IF NOT EXISTS developer (
    id INT NOT NULL AUTO_INCREMENT,
    form_version VARCHAR(40),
    human_readable_question TEXT,
    human_readable_response TEXT,
    last_answered DATETIME,
    response VARCHAR(120),
    variable_name VARCHAR(40),
    user VARCHAR(40),
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (form_version, response, variable_name, user)
);

CREATE TABLE IF NOT EXISTS researcher (
    id INT NOT NULL AUTO_INCREMENT,
    form_version VARCHAR(40),
    human_readable_question TEXT,
    human_readable_response TEXT,
    last_answered DATETIME,
    response VARCHAR(120),
    variable_name VARCHAR(40),
    user VARCHAR(40),
    PRIMARY KEY (id),
    UNIQUE KEY compound_unique (form_version, response, variable_name, user)
);






