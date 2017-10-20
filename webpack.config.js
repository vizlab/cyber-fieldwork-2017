const path = require('path');
const webpack = require('webpack');

const options = {
  entry: {
    bundle: './front/src/main.js'
  },
  output: {
    path: path.join(__dirname, 'front/public'),
    filename: '[name].js'
  },
  devServer: {
    open: false,
    contentBase: path.join(__dirname, 'front/public'),
    historyApiFallback: true
  },
  module: {
    rules: [
      {
        test: /\.js[x]?$/,
        use: [
          {
            loader: 'babel-loader',
            options: {
              cacheDirectory: true,
              presets: ['env']
            }
          }
        ],
        exclude: /node_modules/
      }
    ]
  },
  node: {
    fs: 'empty',
  },
};

if (process.env.NODE_ENV === 'production') {
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({'process.env': {NODE_ENV: '"production"'}}),
    new webpack.optimize.UglifyJsPlugin({sourceMap: true, compress: {warnings: false}}),
    new webpack.LoaderOptionsPlugin({minimize: true})
    ]);
} else {
  module.exports.devtool = 'inline-source-map';
}

module.exports = options;