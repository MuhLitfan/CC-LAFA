const mysql = require('mysql2');

require('dotenv').config()

if (!process.env.DATABASE_PASS) {
  console.error('Error: DATABASE_PASS environment variable is not set.');
  process.exit(1);
}

const db_pass = process.env.DATABASE_PASS;

const connection = mysql.createConnection({
  host: '10.0.0.221',
  user: 'lafa',
  password: db_pass,
  database: 'nodejs'
});

// Debugging: Check if the connection is established successfully

connection.connect(err => {
  if (err) {
    console.error('Error connecting to MySQL:', err.stack);
    return;
  }
  console.log('Connected to MySQL as ID', connection.threadId);
});

module.exports = connection;