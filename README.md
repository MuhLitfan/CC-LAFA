# CC-LAFA

## Deployment

**Environment =**

- Cloud Computing Platform : [Openstack](https://console.adaptivenetworklab.org)
- Virtual Machine Specification :
1. CPU : 4 Core
2. RAM : 8GB
3. Storage : 50GB
4. OS : Ubuntu 22.04

### Node.js Installation

Node.js is for running the web application, built with JavaScript. The command bellow is how to install Node.js

```bash
apt install npm
```

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

### MariaDB Setup Database


```bash
CREATE USER 'lafa'@'%' IDENTIFIED BY '<DATABASE USER PASS>';
```

```bash
>GRANT ALL PRIVILEGES ON *.* TO 'lafa'@'%' WITH GRANT OPTION;
```

```bash
FLUSH PRIVILEGES;
```

```bash
SELECT host FROM mysql.user WHERE User = 'lafa';
```

```bash
CREATE DATABASE nodejs;
```

```bash
USE nodejs;
```

```bash
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL UNIQUE,
  type VARCHAR(255) NOT NULL
);
```

```bash
ALTER USER 'lafa'@'%' IDENTIFIED BY 'CC-LAFA-1234-M4nt4b7iw4';
```