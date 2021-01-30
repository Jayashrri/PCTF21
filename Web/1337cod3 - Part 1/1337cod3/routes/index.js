var express = require('express');
const path = require('path');
var router = express.Router();

router.get('/', function(req, res, next) {
  res.sendFile(path.join(__dirname, '../index.html'));
});

module.exports = router;
