const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

// Proxy configuration
app.use(
  '/api',
  createProxyMiddleware({
    target: 'http://172.26.8.166:8000',
    changeOrigin: true,
  })
);

// Serve static files from the build directory
app.use(express.static('build'));

// Start the server
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
