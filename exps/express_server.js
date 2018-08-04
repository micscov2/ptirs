express = require('express');
port = 55021;

app = express();

app.get('/', function(req, res) {
    console.log(req);
    res.send("hello world from node-express");
});

app.listen(port, function(req, res) {
    console.log("Lstening on port 55021");
});
