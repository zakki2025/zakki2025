<template>
    <el-container class="container" >
      <el-aside class=“aside” width="200px">
        <el-menu :default-active="activeIndex"
               background-color="#545c64"
               text-color="#000"
               active-text-color="#ffd04b"
               class="el-menu-vertical">
          <el-menu-item index="/VisualData" @click="navigateTo('/VisualData')">
            <i class="el-icon-s-marketing"></i>
            数据可视化</el-menu-item>
          <el-menu-item index="/RecommendSystem" @click="navigateTo('/RecommendSystem')">
            <i class="el-icon-star-off"></i>
            推荐系统</el-menu-item>
          <el-menu-item index="/ShopsAround" @click="navigateTo('/ShopsAround')">
            <i class="el-icon-star-on"></i>
            周边店铺</el-menu-item>
          <!-- 其他菜单项 -->
        </el-menu>
      </el-aside>
      <el-container>
        <el-header class="header">
<!--        <div class="logo">My Admin</div>-->
        <div class="header-content">
          <div class="current-path">
            当前路径: {{ $route.path }}
          </div>

          <div class="user-info">
            <img :src="avatarUrl" alt="Avatar" class="avatar">
            <span class="username">{{ username }}</span>
            <el-button type="text" >退出</el-button>
          </div>
        </div>
      </el-header>

  
        <el-main class="main">
          <router-view></router-view>
        </el-main>
      </el-container>
  
    </el-container>
  </template>
  
  <script>
  export default {
    data() {
      return {
        activeIndex: '/VisualData',
        username: '用户001',
        avatarUrl: require('D:\\DesktopFiles\\vue_test\\myvue\\src\\assets\\avatar.png')

      };
    },
    methods: {
      navigateTo(path) {
        console.log(this.activeIndex);
        if (this.$route.path !== path) {
          this.activeIndex = path;
          this.$router.push(path);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .aside{
    background-color: #545c64;
  }

  .container{
    height: 100vh;
    border: 1px solid #eee;
  }
  
  .header {
    background-color: #ffffff;
    text-align: center;
    line-height: 60px;
    border-bottom: 1px solid #ebeef5;
  }
  
  .logo {
    font-size: 20px;
    font-weight: bold;
  }
  
  .main {
    padding: 20px;
  }

  .header-content {
  display: flex;
  /*justify-content: space-between;*/
  /*align-items: center;*/
  /*width: 100%;*/
}

.user-info {
  display: flex;
  align-items: center;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}

.username {
  margin-right: 10px;
}

.current-path {
  margin-right: auto;   /* 当前路径是靠左的 */
  /*padding-left: 20px;*/
}
  </style>
  
  