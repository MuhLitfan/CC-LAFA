#!/usr/bin/env node

const express = require('express');
const session = require('express-session');
const MemoryStore = require('memorystore')(session)

const {createRestApi} = require('./backend/api.js');
const {createViewApi} = require('./frontend/api.js');

const app = express();

require('dotenv').config()

if (!process.env.COOKIES_SECRET) {
  console.error('Error: COOKIES_SECRET environment variable is not set.');
  process.exit(1);
}

// app.use(session({
// 	secret: 'secret',
// 	resave: true,
// 	saveUninitialized: true
// }));

const cookies_secret = process.env.COOKIES_SECRET;

app.use(session({
    cookie: { maxAge: 86400000 },
    store: new MemoryStore({
      checkPeriod: 86400000 // prune expired entries every 24h
    }),
    resave: false,
	saveUninitialized: true,
    secret: cookies_secret
}))

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
