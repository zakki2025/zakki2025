<template>
  <div>
    <v-chart :option="chartOptions" style="width: 100%; height: 450px;"></v-chart>
  </div>
</template>

<script>
import {getCommentsRank} from "@/api/tour"

export default {
  name: 'ShopCommentsRanking',
  data() {
    return {
      chartOptions: {
        title: {
          text: '周边十大热门店铺'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
          },
        },
        legend: {
          data: ['评论数', '店铺评分'],
        },
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: {
            rotate: 30, // 将标签旋转45度
            interval: 0 // 显示所有标签
          }
        },
        yAxis: [
          {
            type: 'value',
            name: '评论数',
            axisLabel: {
              formatter: '{value} 条'
            },
            position: 'left',
          },
          {
            type: 'value',
            name: '店铺评分',
            max: 5, // 最大值为5
            axisLabel: {
              formatter: '{value} 分'
            },
            position: 'right',
          }
        ],
        series: [
          {
            name: '评论数',
            type: 'bar',
            barWidth: '60%', // 可以调整柱子的宽度
            itemStyle: {
              borderRadius: 10, // 设置圆角
            },
            data: [],
          },
          {
            name: '店铺评分',
            type: 'line',
            yAxisIndex: 1, // 使用第二个y轴
            data: [],
          },
        ],
        grid: {
          containLabel: true
          },
      },
    };
  },
  mounted() {
    getCommentsRank().then(res => {
      console.log(res.data.data);
      this.chartOptions.xAxis.data = res.data.data.map(item => item.商家名称);
      this.chartOptions.series[0].data = res.data.data.map(item => item.评论数量);
      this.chartOptions.series[1].data = res.data.data.map(item => item.评分);

      // 动态生成颜色列表
      const colorList = this.generateColorList(res.data.data.length);
      // 应用颜色列表到柱状图的itemStyle中
      this.chartOptions.series[0].itemStyle.color = function(params) {
        return colorList[params.dataIndex];
      };
    })
  },
  methods: {
    generateColorList(length) {
      const colors = ['#5470C6', '#91CC75', '#EE6666', '#73C0DE', '#3BA272'];
      const colorList = [];
      for (let i = 0; i < length; i++) {
        colorList.push(colors[i % colors.length]);
      }
      return colorList;
    }
  }
};
</script>

<style scoped>
/* 添加一些样式使图表看起来更好 */
</style>