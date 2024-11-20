const path = require('path');

// http://localhost:3000/
const createViewApi = app => {
    app.get('/', async (request, response) => {
        if (request.session.userId && request.session.loggedin) {
            return response.sendFile(path.join(__dirname, 'home.html'));
        } else if (request.session.userId && request.session.admin) {
            return response.sendFile(path.join(__dirname, 'admin.html'));
        } else {
            return response.sendFile(path.join(__dirname, 'login.html'));
        }
    });
};

module.exports = {
    createViewApi
};