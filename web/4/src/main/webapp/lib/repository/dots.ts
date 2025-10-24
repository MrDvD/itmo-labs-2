import type { DotParams, DotStatus } from "lib/dto.js";
import { createContext } from "svelte";

export type ItemRepository<Item, Params> = {
  get: () => Promise<Item[]>;
  post: (data: Params) => Promise<Item>;
  delete: () => Promise<void>;
};

export const [ getItemContext, setItemContext ] = createContext<ItemRepository<DotStatus, DotParams>>();

const url = {
  getDots: "/dots",
  postDot: "/dots",
  deleteDots: "/dots",
};

export const DotsRepository = (): ItemRepository<DotStatus, DotParams> => ({
  get: async (): Promise<DotStatus[]> => {
    const response = await fetch(url.getDots, {
      method: "GET",
    });
    if (!response.ok) {
      throw new Error(`GET request to ${url.getDots} failed with status ${response.status}`);
    }
    return await response.json();
  },
  post: async (data: DotParams): Promise<DotStatus> => {
    const response = await fetch(url.postDot, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error(`POST request to ${url.postDot} failed with status ${response.status}`);
    }
    return await response.json();
  },
  delete: async (): Promise<void> => {
    const response = await fetch(url.deleteDots, {
      method: "DELETE",
    });
    if (!response.ok) {
      throw new Error(`DELETE request to ${url.deleteDots} failed with status ${response.status}`);
    }
  }
});