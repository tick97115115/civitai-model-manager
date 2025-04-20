<script setup lang="ts">
import type { ModelId, ModelsRequestOpts } from "../models/models_endpoint";
import { models_response } from "../models/models_endpoint";
import { validate_all_records } from "../models/__test__/load_data_list";
import { type } from "arktype";
import { ElMessage } from "element-plus";
import { ref } from "vue";
import ky from "ky";

async function print() {
    console.log("23");
}

const input3 = ref("");
const select = ref("");
const MODELS_ENDPOINT = "https://civitai.com/api/v1/models";

const model_ids = ref<Array<ModelId>>([]);
const next_page = ref<null | string>(null);
async function search(opts: ModelsRequestOpts = {}) {
    const params = new URLSearchParams();
    for (const [key, value] of Object.entries(opts)) {
        if (Array.isArray(value)) {
            value.forEach((v) => params.append(key, String(v)));
        } else {
            params.append(key, String(value));
        }
    }
    const res = await ky.get(MODELS_ENDPOINT, {
        searchParams: params,
        mode: "cors",
    });
    if (!res.ok) {
        return ElMessage({
            message: res.statusText,
            type: "warning",
        });
    }
    const json = await res.json();
    const data = models_response(json);
    if (data instanceof type.errors) {
        // hover out.summary to see validation errors
        return ElMessage({
            message: data.summary,
            type: "warning",
        });
    } else {
        model_ids.value = data.items;
        next_page.value = data.metadata.nextPage ?? null;
        console.log(next_page.value);
    }
}

async function load() {
    if (next_page.value === null) {
        //
        return;
    }
    const res = await ky.get(next_page.value);
    if (!res.ok) {
        ElMessage({
            message: res.statusText,
            type: "warning",
        });
    }
    const json = await res.json();
    const data = models_response(json);
    if (data instanceof type.errors) {
        // hover out.summary to see validation errors
        ElMessage({
            message: data.summary,
            type: "warning",
        });
        return;
    }

    model_ids.value.push(...data.items);
    next_page.value = data.metadata.nextPage ?? null;
    return;
}
</script>

<template>
    <el-container>
        <!-- <el-header>Header</el-header> -->
        <el-main>
            <KeepAlive>
                <el-row
                    :gutter="10"
                    v-infinite-scroll="load"
                    style="overflow: auto; height: 85vh"
                >
                    <el-col
                        :xs="12"
                        :sm="8"
                        :md="6"
                        :lg="4"
                        :xl="3"
                        v-for="model_id in model_ids"
                        :key="model_id.id"
                    >
                        <el-card shadow="hover">
                            <template #header>{{ model_id.name }}</template>
                            <img
                                loading="lazy"
                                :src="
                                    model_id.modelVersions[0]?.images[0]?.url ??
                                    null
                                "
                                style="width: 100%"
                            />
                        </el-card>
                    </el-col> </el-row
            ></KeepAlive>
        </el-main>

        <!-- <el-divider style="margin: 0%" /> -->

        <el-footer class="footer">
            <el-input
                v-model="input3"
                placeholder="Please input"
                class="input-with-select searchbar"
            >
                <template #prepend>
                    <el-select
                        v-model="select"
                        placeholder="Select"
                        style="width: 115px"
                    >
                        <el-option label="Restaurant" value="1" />
                        <el-option label="Order No." value="2" />
                        <el-option label="Tel" value="3" />
                    </el-select>
                </template>
                <template #append>
                    <el-button @click="search()">
                        <template #icon>
                            <el-icon><Search /></el-icon> </template
                    ></el-button>
                </template>
            </el-input>
        </el-footer>
    </el-container>
</template>

<style lang="scss" scoped>
.footer {
    height: 13vh;
    display: flex;
    justify-content: center;
    align-items: start;
}
.searchbar {
    max-width: 600px;
}
</style>
