const path = require('path');
let connectionRequest = require('./database.js');

const createRestApi = app => {
    // http://localhost:3000/auth
    connection = connectionRequest();
    
    app.post('/auth', function(request, response) {
        if (request.session.userId) {
            response.json({result: 'ERROR', message: 'User already logged in.'});
        } else {
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
                        // Store user session ID
                        const user = results[0];
                        request.session.userId = user.id;
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
                                } else {
                                    response.send('Your account is not authorized to access this page!');
                                    response.end();
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
        }
    });

    // http://localhost:3000/logout
    app.get('/logout', async (request, response) => {
        if (request.session.userId) {
            delete request.session.userId;
            response.cookie('session_cookie', '', {expires: new Date(0)});
            response.json({result: 'SUCCESS'});
        } else {
            response.json({result: 'ERROR', message: 'User is not logged in.'});
        }
    });

    // http://localhost:3000/home
    app.get('/home', function(request, response) {
        // If the user is loggedin
        if ((request.session.loggedin || request.session.admin) && request.session.userId) {
            // Output username
            // response.send('Welcome back, ' + request.session.username + '!');
            response.sendFile(path.join(__dirname , '../frontend/home.html'));
        } else {
            // Not logged in
            response.send('Please login to view this page!');
        }
    });

    // http://localhost:3000/admin
    app.get('/admin', function(request, response) {
        // If the user is loggedin
        if (request.session.admin && request.session.userId) {
            // Output username
            response.sendFile(path.join(__dirname , '../frontend/admin.html'));
        } else if (request.session.loggedin && request.session.userId) {
            // Not authorized
            response.send('You are not authorized to view this page!');
        } else {
            // Not logged in
            response.send('Please login to view this page!');
        }
    });

    // http://localhost:3000/dashboard
    app.get('/dashboard', function(request, response) {
        // If the user is loggedin
        if (request.session.admin && request.session.userId) {
            // Output username
            response.sendFile(path.join(__dirname , '../frontend/dashboard.html'));
        } else if (request.session.loggedin && request.session.userId) {
            // Not authorized
            response.send('You are not authorized to view this page!');
        } else {
            // Not logged in
            response.send('Please login to view this page!');
        }
    });

    // http://localhost:3000/about
    app.get('/about', function(request, response) {
        // If the user is loggedin
        if ((request.session.loggedin || request.session.admin) && request.session.userId) {
            // Output username
            response.sendFile(path.join(__dirname , '../frontend/about.html'));
        } else {
            // Not logged in
            response.send('Please login to view this page!');
        }
    });

}

module.exports = {
    createRestApi
};