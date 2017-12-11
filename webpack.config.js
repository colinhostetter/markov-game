var webpack = require('webpack');
var path = require('path');
var autoprefixer = require('autoprefixer');

var BUILD_DIR = path.resolve(__dirname, 'static');
var APP_DIR = path.resolve(__dirname, 'client');

var config = {
  entry: APP_DIR + '/app.jsx',
  output: {
    path: BUILD_DIR,
    filename: 'bundle.js'
  },
  resolve: {
    extensions: ['.js', '.jsx']
  },
  module: {
    loaders: [
      { test: /\.jsx?$/, loader: 'babel-loader' },
      { test: /\.css$/, exclude: /node_modules/, use: [
        { loader: 'style-loader' },
        { loader: 'css-loader' },
        { loader: 'postcss-loader' }
      ] }
    ]
  },
  plugins: [

  ]
};

module.exports = config;