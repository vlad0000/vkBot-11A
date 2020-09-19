const express = require('express');
const bodyParser = require('body-parser');
const {Botact} = require('botact');

const app = express();

app.use(bodyParser.json());