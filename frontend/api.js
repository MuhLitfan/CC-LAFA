const path = require('path');

// http://localhost:3000/
const createViewApi = app => {
    app.get('/', async (request, response) => {
        if (request.session.userId) {
            return response.sendFile(path.join(__dirname, 'home.html'));
        } else {
            return response.sendFile(path.join(__dirname, 'login.html'));
        }
    });
};

module.exports = {
    createViewApi
};