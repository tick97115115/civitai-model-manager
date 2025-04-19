<script setup lang="ts">
import { RouterView } from "vue-router";
import Sidebar from "@/components/Sidebar.vue";
</script>

<template>
    <div class="common-layout">
        <el-container>
            <el-aside width="300px">
                <Sidebar></Sidebar>
            </el-aside>
            <RouterView />
            <!--  Do not delete these commented code, they are template for view
            <el-container>
        <el-header>Header</el-header>
        <el-main>Main</el-main>
        <el-footer>Footer</el-footer>
      </el-container> -->
        </el-container>
    </div>
</template>

<style lang="less" scoped>
.common-layout {
    width: 100vw;
    height: 100vh;
    overflow: hidden;
}
</style>
