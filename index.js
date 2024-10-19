const express = require('express');
const session = require('express-session');

const {createRestApi} = require('./backend/api.js');
const {createViewApi} = require('./frontend/api.js');

const app = express();

app.use(session({
	secret: 'secret',
	resave: true,
	saveUninitialized: true
}));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('frontend'));

createRestApi(app);
createViewApi(app);

const PORT = '3000';
const HOST = '0.0.0.0';
app.listen(PORT, HOST, () => {
  console.log(`Server running at http://${HOST}:${PORT}/`);
});