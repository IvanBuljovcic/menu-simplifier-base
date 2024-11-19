"use client";

import { Item } from "@/app/page";

export const useGetUniqueIngredients = (items: Item[]) => {
  const allIngredients = items?.flatMap((item) => item.ingredients);
  const uniqueIngredients = [...new Set(allIngredients)].filter((ingredient) => ingredient !== "").sort();

  return uniqueIngredients;
};
