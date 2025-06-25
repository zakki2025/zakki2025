const { defineConfig } = require('@vue/cli-service')


module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8999, // 端口号配置
    // open: true // 自动打开浏览器
    proxy: {
      "/api": {
        target: "http://localhost:8080",
        changeOrigin: true,
        ws: false,
        pathRewrite: {
          "^/api": ""
        }
      }
    }
  }
})


