<template>
  <div ref="radarChart" style="width: 600px; height: 500px;"></div>
</template>

<script>
import * as echarts from 'echarts';
import { getScoresRadar } from "@/api/tour"; // 导入获取雷达图数据的API方法

export default {
  name: 'RadarChart',
  mounted() {
    this.fetchDataAndInitChart(); // 在组件挂载后获取数据并初始化图表
  },
  methods: {
    fetchDataAndInitChart() {
      getScoresRadar().then(response => { // 调用API获取数据
        const data = response.data; // 假设返回的数据格式与之前提供的JSON格式一致
        this.initChart(data); // 使用获取的数据初始化图表
      }).catch(error => {
        console.error('Error fetching radar chart data:', error);
      });
    },
    initChart(data) {
      const chart = echarts.init(this.$refs.radarChart);

      const option = {
        title: {
          text: '店铺评价雷达图'
        },
        tooltip: {},
        legend: {
          data: ['最大值', '最小值', '平均值']
        },
        radar: {
          shape: 'polygon',
          name: {
            textStyle: {
              color: '#fff',
              backgroundColor: '#999',
              borderRadius: 3,
              padding: [3, 5]
            }
          },
          indicator: [
            { name: '总评分', max: 5 },
            { name: '口味', max: 5 },
            { name: '服务', max: 5 },
            { name: '环境', max: 5 }
          ]
        },
        series: [{
          name: '评分',
          type: 'radar',
          data: [
            {
              value: [data['最大值']['总评分'], data['最大值']['口味'], data['最大值']['服务'], data['最大值']['环境']],
              name: '最大值'
            },
            {
              value: [data['最小值']['总评分'], data['最小值']['口味'], data['最小值']['服务'], data['最小值']['环境']],
              name: '最小值'
            },
            {
              value: [data['平均值']['总评分'], data['平均值']['口味'], data['平均值']['服务'], data['平均值']['环境']],
              name: '平均值'
            }
          ]
        }]
      };

      chart.setOption(option);
    }
  }
};
</script>

<style scoped>
/* 你可以在这里添加一些样式 */
</style>
