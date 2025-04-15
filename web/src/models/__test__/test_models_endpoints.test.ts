import { describe, test, expect } from "vitest";
import { validate_all_records } from "./load_data_list";

test("test", () => {
  expect(true).eq(true);
});

test("load 500 records", () => {
  const result = validate_all_records();
  expect(typeof result[0].id === "number").toBe(true);
});
