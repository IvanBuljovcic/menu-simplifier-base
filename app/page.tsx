"use client";

import Combobox from "@/components/combobox";
import { Checkbox } from "@/components/ui/checkbox";
import data from "@/data/menu.json";
import { useEffect, useState } from "react";

export type Item = {
  name: string;
  ingredients: string[];
  price: string | "Unknwon";
};

export default function Home() {
  const [menuItems, setMenuItems] = useState(data || []);

  const allIngredients = menuItems?.flatMap((item) => item.ingredients);
  console.log("allIngredients: ", allIngredients);
  const uniqueIngredients = [...new Set(allIngredients)].filter((ingredient) => ingredient !== "").sort();

  useEffect(() => {
    if (data) {
      setMenuItems(data);
    }
  }, []);

  const renderEmpty = () => <h1>No items</h1>;

  const renderItems = () => (
    <div className="flex flex-col justify-center items-center w-full">
      <h1 className="mb-5 text-5xl">Items: {data.length}</h1>

      <div className="gap-3 grid grid-cols-4">
        {uniqueIngredients.map((ing) => (
          <div className="flex items-center space-x-2" key={ing}>
            <Checkbox id={ing} />
            <label
              htmlFor={ing}
              className="peer-disabled:opacity-70 font-medium text-sm leading-none peer-disabled:cursor-not-allowed"
            >
              {ing}
            </label>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="justify-items-center items-center mx-auto py-8 container">
      {menuItems && menuItems?.length && renderItems()}

      {!menuItems && renderEmpty()}
    </div>
  );
}
