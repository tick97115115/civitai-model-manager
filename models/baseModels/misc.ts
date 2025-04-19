import { type } from "arktype";

// https://www.jsondiff.com/ 找到共有属性名

export const model_types = type(
  "'Checkpoint' | 'TextualInversion' | 'Hypernetwork' | 'AestheticGradient' | 'LORA' | 'Controlnet' | 'Poses' | 'LoCon' | 'DoRA' | 'Other' | 'MotionModule' | 'Upscaler' | 'VAE' | 'Wildcards' | 'Workflows' | 'Detection'"
);
export type ModelTypes = typeof model_types.infer;

export const models_request_period = type(
  "'AllTime' | 'Day' | 'Week' | 'Month' | 'Year'"
);
export type ModelsRequestPeriod = typeof models_request_period.infer;

export const allowCommercialUse = type(
  "'Image' | 'RentCivit' | 'Rent' | 'Sell' | 'None'"
);
export type AllowCommercialUse = typeof allowCommercialUse.infer;

export const models_request_sort = type(
  "'Highest Rated' | 'Most Downloaded' | 'Newest'"
);
export type ModelsRequestSort = typeof models_request_sort.infer;

export const nsfwLevel = type("'None' | 'Soft' | 'Mature' | 'X' | 'Blocked'");
export type NsfwLevel = typeof nsfwLevel.infer;
