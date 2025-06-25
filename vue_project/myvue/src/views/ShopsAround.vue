<template>
    <div class="tours-container">
      <el-card class="box-card">
  <div slot="header" class="header">
    <span class="header-title">周边店铺管理</span>
    <div class="header-controls">
      <el-input v-model="searchTitle" placeholder="输入标题进行搜索" class="search-input"></el-input>
      <el-button type="primary" @click="fetchData">搜索</el-button>
      <el-button type="success" @click="handleAddTour">添加店铺</el-button>
    </div>
  </div>

  <el-table :data="shops" style="width: 100%">
    <el-table-column prop="商家名称" label="商家名称" width="180"></el-table-column>
    <el-table-column prop="商家ID" label="商家ID" width="150"></el-table-column>
    <el-table-column prop="商家链接" label="商家链接" width="150"></el-table-column>
    <el-table-column prop="标签" label="标签" width="150"></el-table-column>
    <el-table-column prop="位置" label="位置" width="150"></el-table-column>
    <el-table-column prop="评论数量" label="评论数量" width="120"></el-table-column>
    <el-table-column prop="人均消费" label="人均消费" width="120"></el-table-column>
    <el-table-column prop="评分" label="评分" width="120"></el-table-column>
    <el-table-column prop="口味" label="口味" width="120"></el-table-column>
    <el-table-column prop="环境" label="环境" width="120"></el-table-column>
    <el-table-column prop="服务" label="服务" width="120"></el-table-column>
    <el-table-column label="操作" min-width="180">
      <template slot-scope="scope">
        <el-button @click="handleEditTour(scope.row)" type="text" size="small">编辑</el-button>
        <el-button @click="handleDeleteTour(scope.row)" type="text" size="small">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-size="pageSize"
      :total="totalItems"
      layout="total, sizes, prev, pager, next, jumper"
  />

</el-card>
      <el-dialog title="编辑店铺" :visible.sync="dialogVisible">
        <el-form :model="form">
          <el-form-item label="商家名称" :label-width="formLabelWidth">
            <el-input v-model="form.name"></el-input>
          </el-form-item>
          <el-form-item label="商家ID" :label-width="formLabelWidth">
            <el-input v-model="form.alias"></el-input>
          </el-form-item>
          <el-form-item label="商家链接" :label-width="formLabelWidth">
            <el-input v-model="form.alias"></el-input>
          </el-form-item>
          <el-form-item label="标签" :label-width="formLabelWidth">
            <el-input v-model="form.alias"></el-input>
          </el-form-item>
          <el-form-item label="位置" :label-width="formLabelWidth">
            <el-input v-model="form.alias"></el-input>
          </el-form-item>
          <el-form-item label="评论数量" :label-width="formLabelWidth">
            <el-input v-model="form.reviewCount" type="number"></el-input>
          </el-form-item>
          <el-form-item label="评分" :label-width="formLabelWidth">
            <el-input v-model="form.rating" type="number"></el-input>
          </el-form-item>
          <el-form-item label="口味" :label-width="formLabelWidth">
            <el-input v-model="form.rating" type="number"></el-input>
          </el-form-item>
          <el-form-item label="环境" :label-width="formLabelWidth">
            <el-input v-model="form.rating" type="number"></el-input>
          </el-form-item>
          <el-form-item label="服务" :label-width="formLabelWidth">
            <el-input v-model="form.rating" type="number"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSaveTour">保存</el-button>
        </div>
      </el-dialog>
    </div>
  </template>
  
<script>
import {shops} from "@/api/tour"

  export default {
    data() {
    return {
      searchTitle: '',
      tours: [],
      dialogVisible: false,
      form: {},
      formLabelWidth: '100px',
      totalItems: 0,
      currentPage: 1,
      pageSize: 10,
    };
  },

  mounted() {
    this.currentPage = 1
    this.loadData()
  },
  
  methods: {
      fetchData() {
        this.loadData()
      },
      //加载数据
      loadData() {
          shops(this.searchTitle, this.currentPage, this.pageSize).then(res => {
            // console.log(res.data.data.records);
            this.shops = res.data.data.records
            this.totalItems = res.data.data.total
          })
      },
      
      handleCurrentChange(page) {
        this.currentPage = page;
        this.loadData();
      },
      handleSizeChange(size) {
        this.pageSize = size;
        this.loadData();
      },
  }

    
  };
  </script>
  
  <style scoped>
  .tours-container {
    padding: 20px;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
  }

  .dialog-footer {
    text-align: right;
  }

  .header-title {
    font-size: 18px;
    font-weight: bold;
  }

  .header-controls {
    display: flex;
    align-items: center;
  }

  .search-input {
    width: 300px;
    margin-right: 10px; /* Adjust spacing between input and buttons */
  }

  </style>
  
  