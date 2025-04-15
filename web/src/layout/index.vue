<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="300px">
        <Sidebar></Sidebar>
      </el-aside>
      <el-container>
        <el-header>Header</el-header>
        <el-main>Main</el-main>
        <el-footer>Footer</el-footer>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import Sidebar from '@/layout/components/Sidebar/index.vue'
</script>

<style lang="less" scoped>
.common-layout {
  width: 100vw;
  height: 100vh;
  overflow: hidden;

}
</style>