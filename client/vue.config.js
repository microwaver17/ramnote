module.exports = {
    publicPath: './',
    devServer: {
        proxy: {
            '/api/': {
                target: 'http://localhost:5000/'
            }
        }
    },
    configureWebpack: {
        externals: {
            bootstrap: 'bootstrap'
        }
    }
}