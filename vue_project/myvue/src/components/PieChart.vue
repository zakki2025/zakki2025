<template>
    <div>
      <v-chart :option="chartOptions" style="width: 100%; height: 400px;"></v-chart>
    </div>
  </template>
  
  <script>
import {getNumberRank} from "@/api/tour";

  export default {
    name: 'PieChart',
    data() {
      return {
        chartOptions: {
          title: {
            text: '菜品类型分布'
          },
          tooltip: {},
          series: [{
            type: 'pie',
            data: [
              {name:'东京',value:104},
              {name:'大阪',value:81},
              {name:'京都',value:47},
              {name:'横滨',value:51},
              {name:'名古屋',value:62}]
          }]
        },
      };
    },
    mounted() {
      getNumberRank().then(res => {
        console.log(res.data); // 打印整个响应数据
        const pieData = res.data.data.map(item => ({
          name: item.name,
          value: item.value
        }));
        this.chartOptions.series[0].data = pieData;
      }).catch(error => {
        console.error('Error fetching data:', error);
      });
    }
  };

 
  </script>
  
  <style scoped>
  /* 添加一些样式使图表看起来更好 */
  </style>
  
  