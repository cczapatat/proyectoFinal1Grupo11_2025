const express = require('express');
const path = require('path');

const app = express();

app.use(express.static(__dirname + '/dist/web-smartstock'));

app.get('/health', function (req, res) {
    res.send('OK');
});

app.get('/*', function (req, res) {
    res.sendFile(path.join(__dirname + '/dist/web-smartstock/index.html'));
});

const PORT = process.env.PORT || 5000;

app.listen(PORT, '0.0.0.0', function () {
    console.log("Server running on port 5000...");
});
