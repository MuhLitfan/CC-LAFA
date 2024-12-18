module.exports = function () {
 
  require('dotenv').config()

  if (!process.env.DATABASE_PASS) {
    console.error('Error: DATABASE_PASS environment variable is not set.');
    process.exit(1);
  }

  let mysql = require('mysql2')

  let db_pass = process.env.DATABASE_PASS

  //Establish Connection to the DB
  let connection = mysql.createConnection({
      host: 'localhost',
      user: 'lafa',
      password: db_pass,
      database: 'nodejs',
      port: 9906,
      enableKeepAlive: true,
      keepAliveInitialDelay: 10000, // 0 by default.
      waitForConnections: true,
      // Keepalive configuration
      connectTimeout: 10000, // 10 seconds
  });

  //Instantiate the connection
  connection.connect(function (err) {
      if (err) {
          console.log(`connectionRequest Failed ${err.stack}`)
      } else {
          console.log(`DB connectionRequest Successful ${connection.threadId}`)
      }
  });

  //return connection object
  return connection
}