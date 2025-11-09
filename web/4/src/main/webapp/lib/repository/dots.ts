import type { DotParams, DotStatus } from "@lib/dto.js";
import { AppServices } from "@lib/services.js";
import { createContext } from "svelte";

export type ItemRepository<Item, Params> = {
  get: () => Promise<Item[]>;
  post: (data: Params) => Promise<Item>;
  delete: () => Promise<void>;
};

export interface ItemRepositoryBuilder<Item, Params> {
  build(): ItemRepository<Item, Params>
}

export const [ getItemContext, setItemContext ] = createContext<ItemRepositoryBuilder<DotStatus, DotParams>>();

const url = {
  getDots: "/dots",
  postDot: "/dots",
  deleteDots: "/dots",
};

export const DotsRepository = (): ItemRepository<DotStatus, DotParams> => {
  const errorHandler = AppServices.SERVER_ERROR_HANDLER.get();
  return {
    get: async (): Promise<DotStatus[]> => {
      const response = await fetch(url.getDots, {
        method: "GET",
      });
      if (!response.ok) {
        errorHandler.handle(response.json());
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
        errorHandler.handle(response.json());
      }
      return await response.json();
    },
    delete: async (): Promise<void> => {
      const response = await fetch(url.deleteDots, {
        method: "DELETE",
      });
      if (!response.ok) {
        errorHandler.handle(response.json());
      }
    }
  }
};

export class DotsRepositoryFactory {
  public build(): ItemRepository<DotStatus, DotParams> {
    return DotsRepository();
  }
}