<template>
  <div class="recommendation-container">
    <div class="form-container">
      <h2>推荐系统输入</h2>
      <el-form :model="form" label-width="100px">
        <el-form-item label="用户ID">
          <el-input v-model="form.UserID" placeholder="请输入用户ID"></el-input>
        </el-form-item>
        <el-form-item label="场景标签">
          <el-select v-model="form.user_meal_scene" placeholder="请选择场景标签">
            <el-option label="朋友聚会" value="朋友聚会"></el-option>
            <el-option label="家庭聚餐" value="家庭聚餐"></el-option>
            <el-option label="情侣约会" value="情侣约会"></el-option>
            <el-option label="商务宴请" value="商务宴请"></el-option>
            <el-option label="公司团建" value="公司团建"></el-option>
            <el-option label="节日聚餐" value="节日聚餐"></el-option>
            <el-option label="学生聚餐" value="学生聚餐"></el-option>
            <el-option label="主题派对" value="主题派对"></el-option>
            <el-option label="亲子溜娃" value="亲子溜娃"></el-option>
            <el-option label="单人餐" value="单人餐"></el-option>
            <el-option label="单身餐" value="单身餐"></el-option>
            <el-option label="外卖" value="外卖"></el-option>
            <el-option label="工作日" value="工作日"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="关注点">
          <el-select v-model="form.user_focus_point" placeholder="请选择关注点">
            <el-option label="口味" value="口味"></el-option>
            <el-option label="环境" value="环境"></el-option>
            <el-option label="服务" value="服务"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitRecommendation">获取推荐</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="result-container">
      <h2>推荐结果</h2>
      <div v-if="loading">
        <el-skeleton :rows="5" animated></el-skeleton>
      </div>
      <div v-else-if="recommendationList.length > 0">
        <el-table :data="recommendationList" style="width: 100%">
          <el-table-column prop="店铺名称" label="店铺名称" width="200"></el-table-column>
          <el-table-column prop="菜品相似度得分" label="菜品相似度得分" width="150"></el-table-column>
          <el-table-column prop="场景相似度得分" label="场景相似度得分" width="150"></el-table-column>
          <el-table-column prop="关注点相似度得分" label="关注点相似度得分" width="150"></el-table-column>
          <el-table-column prop="总体评分" label="总体评分" width="100"></el-table-column>
          <el-table-column prop="推荐分" label="推荐分" width="100"></el-table-column>
        </el-table>
      </div>
      <div v-else>
        <p>暂无推荐结果</p>
      </div>
    </div>
  </div>
</template>


<script>
// 在 script 标签的顶部引入封装接口函数
import { sendRecommendationRequest } from '@/api/tour';

export default {
  data() {
    return {
      form: {
        UserID: '',
        user_meal_scene: '',
        user_focus_point: ''
      },
      loading: false,
      recommendationList: []
    };
  },
  methods: {
    submitRecommendation() {
      this.loading = true; // 开始加载
      // 使用封装接口函数发送请求
      sendRecommendationRequest(this.form.UserID, this.form.user_meal_scene, this.form.user_focus_point)
      .then(response => {
        // 将后端返回的结果赋值给 recommendationList，用于表格展示
        console.log('后端返回的数据:', response.data);
        this.recommendationList = response.data; // 注意：这里假设后端返回的数据在 response.data 中
        this.loading = false; // 加载完成
      })
      .catch(error => {
        this.loading = false; // 加载失败
        if (error.response) {
            console.error('请求失败，状态码：', error.response.status);
            this.errorMessage = error.response.data.error || '请求失败，请稍后再试。';
        } else if (error.code === 'ECONNABORTED') {
            this.errorMessage = '请求超时，请稍后再试。';
        } else {
            this.errorMessage = '请求失败，请稍后再试。';
        }
        console.error('请求失败：', error);
      });
    }
  }
};
</script>


<style scoped>
.recommendation-container {
  display: flex;
  height: 100vh;
}
.form-container {
  flex: 1;
  padding: 20px;
}
.result-container {
  flex: 1;
  padding: 20px;
  border-left: 1px solid #ccc;
}
</style>