import { promises as fs } from "fs";
import List from "@/components/list";

export type Item = {
  name: string;
  ingredients: string[];
  price: string | "Unknown";
  image?: string;
  id: string;
};

export default async function Home() {
  const file = await fs.readFile(process.cwd() + "/data/menu.json", "utf8");
  const data = JSON.parse(file);

  return (
    <div className="justify-items-center items-center mx-auto py-8 container">
      <List data={data} />
    </div>
  );
}
