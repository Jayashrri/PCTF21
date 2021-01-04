var express = require('express');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var indexRouter = require('./routes/index');
var submitRouter = require('./routes/submit');

var app = express();

// view engine setup

app.use(logger('dev'));
app.use(express.json({limit: '500'}));
app.use(cookieParser());

app.use('/', indexRouter);
app.use('/submit', submitRouter);

module.exports = app;
