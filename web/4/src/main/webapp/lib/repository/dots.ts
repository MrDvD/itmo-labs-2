import type { DotParams, DotStatus } from "lib/dto.js";
import { DefaultErrorHandler, type ServerErrorHandler } from "lib/errors/handler.js";
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

export const DotsRepository = (errorHandler: ServerErrorHandler): ItemRepository<DotStatus, DotParams> => {
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

export const DefaultDotsRepository = () => (DotsRepository(new DefaultErrorHandler()))