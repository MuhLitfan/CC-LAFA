const express = require('express');
const session = require('express-session');
const path = require('path');
const connection = require('./config/database');

const app = express();

app.use(session({
	secret: 'secret',
	resave: true,
	saveUninitialized: true
}));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'static')));

// http://localhost:3000/
app.get('/', function(request, response) {
	// Render login template
	response.sendFile(path.join(__dirname + '/login.html'));
});

// http://localhost:3000/auth
app.post('/auth', function(request, response) {
	// Capture the input fields
	let username = request.body.username;
	let password = request.body.password;
	// Ensure the input fields exists and are not empty
	if (username && password) {
		// Execute SQL query that'll select the users from the database based on the specified username and password
		connection.query('SELECT * FROM users WHERE username = ? AND password = ?', [username, password], function(error, results) {
			// If there is an issue with the query, output the error
			if (error) throw error;
			// If the account exists
			if (results.length > 0) {
				// Authenticate the user
				request.session.username = username;
                // Extract the user type from the results
                let type = results[0].type;
				// Redirect to home page
				connection.query('SELECT * FROM users WHERE type = ?', [type], function(error, results) {
					request.session.type = type;
					if (results.length > 0) {
						if (type == 'admin') {
							request.session.admin = true;
							response.redirect(301, '/admin');
						}
						else if (type == 'user') {
							request.session.loggedin = true;
							response.redirect(301, '/home');
						}
					} else {
						response.send('Your account is not authorized to access this page!');
						response.end();
					}
				});
			} else {
				response.send('Incorrect Username and/or Password!');
				response.end();
			}			
		});
	} else {
		response.send('Please enter Username and Password!');
		response.end();
	}
});

// http://localhost:3000/home
app.get('/home', function(request, response) {
	// If the user is loggedin
	if (request.session.loggedin) {
		// Output username
		response.send('Welcome back, ' + request.session.username + '!');
	} else {
		// Not logged in
		response.send('Please login to view this page!');
	}
	response.end();
});

// http://localhost:3000/admin
app.get('/admin', function(request, response) {
	// If the user is loggedin
	if (request.session.admin) {
		// Output username
		response.send('Welcome, ' + request.session.username + '!' + '\n' + 'You are an admin!');
	} else {
		// Not logged in
		response.send('Please login to view this page!');
	}
	response.end();
});

const PORT = '3000';
const HOST = '0.0.0.0';
app.listen(PORT, HOST, () => {
  console.log(`Server running at http://${HOST}:${PORT}/`);
});