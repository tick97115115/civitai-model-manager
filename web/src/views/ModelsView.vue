<template>
    <el-container>
        <!-- <el-header>Header</el-header> -->
        <el-main>Main</el-main>
        <el-footer>Footer</el-footer>
    </el-container>
</template>

<script setup lang="ts">
import { ModelId } from "../models/models_endpoint";
import { validate_all_records } from "../models/__test__/load_data_list";
const model_ids = validate_all_records();
// for (let index = 0; index < model_ids.length; index++) {
//     const element = model_ids[index] as ModelId;
//     element as ModelId;
// }
</script>
