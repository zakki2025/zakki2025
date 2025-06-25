<template>
  <div ref="treemapChart" style="width: 100%; height: 600px;"></div>
</template>

<script>
import * as echarts from 'echarts';
import { getShopsLocation } from "@/api/tour"; 

export default {
  name: 'TreemapChart',
  data() {
    return {
      chart: null,
      districtsData: {}, // 存储所有商圈的数据
      currentDistrict: '', // 当前选中的商圈
    };
  },
  mounted() {
    this.fetchDataAndInitChart();
  },
  methods: {
    fetchDataAndInitChart() {
      getShopsLocation().then(response => {
        this.districtsData = response.data; // 存储所有商圈的数据
        this.initChart(); // 初始化图表
      }).catch(error => {
        console.error('Error fetching treemap chart data:', error);
      });
    },
    initChart() {
      this.chart = echarts.init(this.$refs.treemapChart);
      const option = {
        title: {
          text: '商圈美食分布'
        },
        tooltip: {
          formatter: '{b}: {c}'
        },
        series: [{
          type: 'treemap',
          data: this.getTopLevelData(),
          label: {
            show: true,
            formatter: '{b}'
          },
          itemStyle: {
            borderColor: '#fff',
            borderWidth: 1
          },
          drillDownIcon: '▶', // 显示点击图标
          emphasis: {
            itemStyle: {
              borderColor: '#fff',
              borderWidth: 2
            }
          },
          on: {
            click: this.drillDown // 点击事件
          }
        }]
      };
      this.chart.setOption(option);
    },
    getTopLevelData() {
      const topLevelData = [];
      Object.keys(this.districtsData).forEach(district => {
        const districtData = this.districtsData[district];
        const value = Object.values(districtData).reduce((sum, item) => sum + item.数量, 0);
        topLevelData.push({
          name: district,
          value: value,
          children: Object.entries(districtData).map(([key, { 数量 }]) => ({
            name: key,
            value: 数量
          }))
        });
      });
      return topLevelData;
    },
    drillDown(params) {
      this.currentDistrict = params.name; // 设置当前选中的商圈
      this.updateChartWithDistrictData(); // 更新图表为当前商圈的具体美食分布
    },
    updateChartWithDistrictData() {
      const districtData = this.districtsData[this.currentDistrict];
      const data = Object.entries(districtData).map(([name, { 数量 }]) => ({
        name,
        value: 数量
      }));
      this.chart.setOption({
        series: [{
          data: data,
          name: this.currentDistrict
        }]
      });
    }
  },
  beforeDestroy() {
    if (this.chart) {
      this.chart.dispose();
    }
  }
};
</script>

<style scoped>
/* 你可以在这里添加一些样式 */
</style>