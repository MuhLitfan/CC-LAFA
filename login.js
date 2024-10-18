const express = require('express');
const connection = require('./config/database');

const app = express();

app.use(express.json());

// Insert a new user
app.post('/users', (req, res) => {
  const { username, type } = req.body;
  connection.query('INSERT INTO users (username, type) VALUES (?, ?)', [username, type], (err, results) => {
    if (err) {
      return res.status(500).send(err);
    }
    res.status(201).send({ id: results.insertId, username, type });
  });
});

// Get all users
app.get('/users', (req, res) => {
  connection.query('SELECT * FROM users', (err, results) => {
    if (err) {
      return res.status(500).send(err);
    }
    res.send(results);
  });
});

const PORT = '3000';
const HOST = '0.0.0.0';
app.listen(PORT, HOST, () => {
  console.log(`Server running at http://${HOST}:${PORT}/`);
});
