"use client";

import { useGetUniqueIngredients } from "@/hooks";
import React, { useMemo, useState } from "react";
import Ingredient from "./ingredient";
import { Item } from "@/app/page";
import { Button } from "./ui/button";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const List = ({ data = [] }: { data?: Item[] }) => {
  const [selected, setSelected] = useState<string[]>([]);

  const uniqueIngredients = useGetUniqueIngredients(data);

  const filteredMenuItems = useMemo(() => {
    if (selected.length === 0) return data;
    return data.filter((item) => selected.every((ing) => item.ingredients.includes(ing)));
  }, [selected, data]);

  const ingredientCounts = useMemo(() => {
    return uniqueIngredients.reduce((acc, ingredient) => {
      let count;
      if (selected?.length > 0) {
        count = filteredMenuItems.filter((item) => item.ingredients.includes(ingredient)).length;
      } else {
        count = data.filter((item) => item.ingredients.includes(ingredient)).length;
      }

      return { ...acc, [ingredient]: count };
    });
  }, [filteredMenuItems, selected, data, uniqueIngredients]);

  // Calculate which ingredients appear together with selected ones
  const validCombinations = useMemo(() => {
    if (selected.length === 0) return uniqueIngredients;

    const matchingItems = data.filter((item) => selected.every((ing) => item.ingredients.includes(ing)));

    const validIngredients = new Set<string>();
    matchingItems.forEach((item) => {
      item.ingredients.forEach((ing) => validIngredients.add(ing));
    });

    return Array.from(validIngredients);
  }, [selected, data, uniqueIngredients]);

  // Get filtered items count based on selection
  const filteredItemsCount = useMemo(() => {
    if (selected.length === 0) {
      return data.length;
    }

    return data.filter((item) => selected.every((ing) => item.ingredients.includes(ing))).length;
  }, [selected, data]);

  const renderEmpty = () => <h1>No items</h1>;

  const handleItemClick = (item: string) => {
    setSelected((prevSelected) =>
      prevSelected.includes(item) ? prevSelected.filter((i) => i !== item) : [...prevSelected, item]
    );
  };

  const renderMenuItem = (item: Item) => (
    <div key={item.id} className="bg-white shadow-md p-4 rounded-lg w-64">
      {item.image && <img srcSet={item.image} alt={item.name} />}

      <h3 className="mb-2 font-semibold text-lg">{item.name}</h3>
      <p className="mb-2 text-gray-600">Price: {item.price}</p>
      <div className="flex flex-wrap gap-1">
        {item.ingredients.map((ing) => (
          <Button
            key={ing}
            className={`text-xs px-2 py-1 rounded ${
              selected.includes(ing) ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-700"
            }`}
            onClick={() => handleItemClick(ing)}
          >
            {ing}
          </Button>
        ))}
      </div>
    </div>
  );

  const renderItems = () => (
    <div className="flex flex-col justify-center items-center w-full">
      <h1 className="mb-5 text-5xl">Items total: {data.length}</h1>

      <div className="columns-4">
        {uniqueIngredients.map((item) => {
          return (
            <Ingredient
              key={item}
              item={item}
              onClick={() => handleItemClick(item)}
              isSelected={selected.includes(item)}
              isValid={validCombinations.includes(item)}
              count={ingredientCounts[item]}
            />
          );
        })}
      </div>
    </div>
  );

  return (
    <div className="container">
      {(!data || !data?.length) && renderEmpty()}

      {data && renderItems()}

      <div className="flex flex-wrap gap-4">{filteredMenuItems.map(renderMenuItem)}</div>
    </div>
  );
};

export default List;
