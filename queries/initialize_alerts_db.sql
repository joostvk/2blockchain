DROP TABLE IF EXISTS users;
CREATE TABLE users(
user_id char(32)  NULL,
device_id  char(36) NOT NULL,
email_address varchar(120) NOT NULL,
pc6 char(6),
huisnummer varchar(20),
huisnummer_toev varchar(20),
mobile_number varchar(20),
smart_meter varchar(40),
energy_gen varchar(10),
CONSTRAINT PK_users PRIMARY KEY CLUSTERED (email_address)
);
CREATE UNIQUE NONCLUSTERED INDEX idx_user_id_notnull
ON users(user_id)
WHERE user_id IS NOT NULL;

DROP TABLE IF EXISTS notifications;
CREATE TABLE notifications
(
device_id char(36)  NOT NULL,
alert_id varchar(36) NOT NUll,
alert_dt datetime NOT NUll,
message [nvarchar](max) NULL,
bubble_view [nvarchar](max) NULL,
url [nvarchar](max) NULL,
pushed_at datetime NULL,
created datetime NOT NULL,
CONSTRAINT PK_notifications PRIMARY KEY CLUSTERED (device_id, alert_id, alert_dt)
);

DROP TABLE IF EXISTS alert_rules;
CREATE TABLE alert_rules
(
user_id char(32) NOT NULL,
alert_id varchar(36) NOT NUll,
max_threshold [float] NULL,
min_threshold [float] NULL,
validity_days [int] NULL,
activated [bit] NOT NULL,
);

DROP TABLE IF EXISTS sm_consumption;
CREATE TABLE sm_consumption
(
user_id char(32)  NULL,
ean_code char(64),
product_groep  char(1),
profile_type char(18),
verbr_datum char(10),
verbr_uur char(2),
verbruik float,
profiel_type varchar(36) NOT NUll
);

DROP TABLE IF EXISTS debit_deficit; 
CREATE TABLE debit_deficit (
partner varchar(8),
contractrek varchar(10),
openstaand_saldo float, 
last_update_time datetime
);

DROP TABLE IF EXISTS [dbo].[woonfit]; 
CREATE TABLE [dbo].[woonfit](
_id [nvarchar](17) NOT NULL,
cipher_id [nvarchar](200) NOT NULL,
co2_calibrating [nvarchar](10) NULL,
absolutePressure [float] NULL,
co2 [float] NULL,
humidity [float] NULL,
noise [float] NULL,
pressure [float] NULL,
temperature [float] NULL,
date_max_temp datetime NULL,
date_min_temp datetime NULL,
health_idx [float]  NULL,
max_temp [float] NULL,
min_temp [float] NULL,
pressure_trend [nvarchar](36) NULL,
temp_trend [nvarchar](10) NULL,
time_utc  datetime NOT NULL,
date_setup datetime NULL,
firmware float NULL,
last_setup datetime NULL,
last_status_store datetime NULL,
last_upgrade datetime NULL,
module_name [nvarchar](36) NULL,
name [nvarchar](max) NULL,
city [nvarchar](max) NULL,
country [nvarchar](max) NULL,
location_lon [float] NULL,
location_lat [float] NULL,
timezone [nvarchar](max) NULL,
type [nvarchar](max) NULL,
wifi_status [float] NULL,
 CONSTRAINT [PK_woonfit] PRIMARY KEY CLUSTERED (_id,cipher_id,time_utc ASC)
 );	



