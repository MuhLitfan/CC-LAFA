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
      host: '10.0.0.221',
      user: 'lafa',
      password: db_pass,
      database: 'nodejs',
      port: 3306
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