const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
    app.use(
        '/api',
        createProxyMiddleware({
            target: 'http://172.26.8.166:8000',
            changeOrigin: true,
        })
    );
};

