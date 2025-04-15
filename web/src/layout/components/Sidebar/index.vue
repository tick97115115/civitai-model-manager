<template>
    <div class="scrollbar">
        <el-scrollbar>
            <el-menu default-active="2" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose"
                unique-opened>
                <el-sub-menu index="1">
                    <template #title>
                        <el-icon>
                            <location />
                        </el-icon>
                        <span>Navigator One</span>
                    </template>
                    <el-menu-item-group>
                        <el-menu-item index="1-1">item one</el-menu-item>
                        <el-menu-item index="1-2">item two</el-menu-item>
                    </el-menu-item-group>
                </el-sub-menu>
            </el-menu>
        </el-scrollbar>
    </div>
</template>

<script setup lang="ts">
import {
    Document,
    Menu as IconMenu,
    Location,
    Setting,
} from '@element-plus/icons-vue'
const handleOpen = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
}

</script>

<style lang="less" scoped>
.scrollbar {
    height: 100vh;
}
</style>
