# CC-LAFA

This project is fully managed and developed by :
- Abiyyu
- Ari
- Faris
- Litfan

## Deployment

**Environment =**

- Cloud Computing Platform : [Openstack](https://console.adaptivenetworklab.org)
- Virtual Machine Specification :
1. CPU : 4 Core
2. RAM : 8GB
3. Storage : 50GB
4. OS : Ubuntu 22.04

## Setting Up Database

### MariaDB Installation

MariaDB is a SQL Database. The command bellow is how to install MariaDB

```bash
apt install mariadb-server
```

### MariaDB Root Initialization
This command will take to multiple prompt for us to fill. Like for the root password, removing test user, and test database, etc.

```bash
sudo mysql_secure_installation
```

### MariaDB Setup Database & User

Create User named `lafa` with password and accesible from any IP and Domain
```bash
CREATE USER 'lafa'@'%' IDENTIFIED BY '<DATABASE USER PASS>';
```

Grant all privileges on user `lafa`
```bash
>GRANT ALL PRIVILEGES ON *.* TO 'lafa'@'%' WITH GRANT OPTION;
```

Update privileges
```bash
FLUSH PRIVILEGES;
```

List Allowed Host who can accessed User `lafa`, to make sure we can accessed it from Any IP & Domain
```bash
SELECT host FROM mysql.user WHERE User = 'lafa';
```

Create `nodejs` database
```bash
CREATE DATABASE nodejs;
```

Get into `nodejs` database
```bash
USE nodejs;
```

Create `users` table in `nodejs` database
```bash
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL UNIQUE,
  type VARCHAR(255) NOT NULL
);
```

## Setting Up Database Manager

### PHPMyAdmin & Apache2 Installation

```bash
sudo apt install phpmyadmin apache2
```

### PHPMyAdmin Setup and Integration to MariaDB

Connect PHPMyAdmin to MariaDB, edit `/etc/phpmyadmin/config-db.php`
```bash
sudo apt install phpmyadmin apache2
```