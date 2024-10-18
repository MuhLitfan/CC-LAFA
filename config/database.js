const db_pass = console.log(process.env.DATABASE_PASS);

const mysql = require('mysql2');

const connection = mysql.createConnection({
  host: '10.0.0.221',
  user: 'lafa',
  password: 'CC-LAFA-1234-M4nt4b7iw4',
  database: 'nodejs'
});

connection.connect(err => {
  if (err) {
    console.error('Error connecting to MySQL:', err.stack);
    return;
  }
  console.log('Connected to MySQL as ID', connection.threadId);
});

module.exports = connection;
