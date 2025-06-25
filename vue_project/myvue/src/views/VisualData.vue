<template>
  <div>
    <el-row :gutter="15">
      <!-- Top left chart (Bar Chart) -->
      <el-col :span="12">
        <div class="chart" style="height: 400px;">
          <CommentsBarChart/>
        </div>
      </el-col>
      <!-- Top right chart (Pie Chart) -->
      <el-col :span="12">
        <div class="chart" style="height: 350px;">
          <PieChart/>
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <div class="chart" style="height: 400px;">
          <RadarChart/>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="chart" style="height: 300px;">
          <TreemapChart/>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import CommentsBarChart from "@/components/CommentsBarChart";
import PieChart from "@/components/PieChart";
import RadarChart from "@/components/RadarChart";
import TreemapChart from "@/components/TreemapChart";

export default {
  name: 'VisualData',
  components: { CommentsBarChart , PieChart , RadarChart , TreemapChart},
};
</script>

<style scoped>
.chart {
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  border-radius: 10px;
}
</style>
