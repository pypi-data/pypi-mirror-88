const HtmlWebpackPlugin = require('html-webpack-plugin');
const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
module.exports = {
mode: 'development',
entry: {
    'pivot': './src/index.js'
},
output: {
    filename: '[name].js',
    path: path.resolve(__dirname, '../browser/static/pivot'),
},
module: {
    rules: [
        {
            test: /.(js|jsx|less)$/,
            exclude: /node_modules/,
            use: ['babel-loader']
        },
        {
            test: /.css$/,
            use: [
                // {
                //     loader: MiniCssExtractPlugin.loader, 
                //     options: {
                //         publicPath: ''
                //     }
                // },
                // {
                //     loader: "css-loader"
                // },

                'style-loader', 'css-loader'
            ],
        },
        {
            test: /\.(png|jpe?g|gif)$/,
            loader: 'file-loader',
            options: {
              name: '[name].[ext]',
            },
        },
        {
            test: /\.svg$/,
            use: [
                {
                loader: 'svg-url-loader',
                options: {
                    name: '[name].[ext]',
                    limit: 10000,
                },
                },
            ],
        },
        {
            test: /\.less$/,
            use: [
              {
                loader: "style-loader",
              },
              {
                loader: "css-loader",
              },
              {
                loader: "less-loader",
                options: {
                  lessOptions: {
                    strictMath: true,
                  },
                },
              },
            ],
          },
    ]
},
plugins: [
    new HtmlWebpackPlugin({
        filename: 'index.html',
        template: 'src/index.html'
    }),
    // new MiniCssExtractPlugin()
],
devServer: {
    contentBase: path.resolve(__dirname, '../browser/static/pivot'),
    open: true,
    port: 3000
},
};