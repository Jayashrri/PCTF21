var express = require('express');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var indexRouter = require('./index');

var helmet = require('helmet')

var app = express();

// view engine setup

app.use(helmet({
    contentSecurityPolicy: false,
}));
app.use(logger('dev'));
app.use(express.json({limit: '500'}));
app.use(cookieParser());
app.disable('x-powered-by');
app.disable('etag');
app.set('trust proxy', 'uniquelocal');

app.use('/', indexRouter);


module.exports = app;
