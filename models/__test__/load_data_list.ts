import { type } from "arktype";
import { json_list } from "./500_records";
import { model_id } from "../models_endpoint";
import type { ModelId } from "../models_endpoint";

export function validate_all_records(): Array<ModelId> {
    const data_list: Array<ModelId> = [];
    for (let index = 0; index < json_list.length; index++) {
        const element = json_list[index];
        const out = model_id(element);
        if (out instanceof type.errors) {
            // hover out.summary to see validation errors
            out.throw();
        } else {
            // hover out to see your validated data
            // console.log(`Hello, ${out.name}`)
            data_list.push(out);
        }
    }
    return data_list;
}
