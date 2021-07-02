module.exports = {
    publicPath: './',
    devServer: {
        proxy: {
            '/api/': {
                target: 'http://localhost:51803/'
            }
        }
    },
    configureWebpack: {
        externals: {
            bootstrap: 'bootstrap'
        }
    },
    pluginOptions: {
        electronBuilder: {
            buildOptions: {
                win: {
                    target: [
                        {
                            target: 'portable',
                            arch: ['x64'],
                        }
                    ]
                }
            }
        }
    }
}