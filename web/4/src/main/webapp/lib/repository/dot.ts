import type { DotParams, DotStatus } from "@lib/dto.js";
import { AppServices } from "@lib/services.js";
import { createContext } from "svelte";
import type { Repository, RepositoryBuilder } from "./util.js";

export interface ItemRepository<Item, Params> extends Repository<Item, Params> {
  get(): Promise<Item[]>;
  post(data: Params): Promise<Item>;
  delete(): Promise<void>;
};

export interface DotsRepositoryUrl {
  get: string;
  post: string;
  delete: string;
}

export const [ getItemContext, setItemContext ] = createContext<RepositoryBuilder<DotStatus, DotParams, ItemRepository<DotStatus, DotParams>>>();

export class DotsRepository implements ItemRepository<DotStatus, DotParams> {
  private errorHandler = AppServices.SERVER_ERROR_HANDLER.get();

  constructor(private url: DotsRepositoryUrl) {}

  public async get(): Promise<DotStatus[]> {
    const response = await fetch(this.url.get, {
      method: "GET",
    });
    if (!response.ok) {
      this.errorHandler.handle(response.json());
    }
    return await response.json();
  }
  public async post(data: DotParams): Promise<DotStatus> {
    const response = await fetch(this.url.post, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      this.errorHandler.handle(response.json());
    }
    return await response.json();
  }
  public async delete(): Promise<void> {
    const response = await fetch(this.url.delete, {
      method: "DELETE",
    });
    if (!response.ok) {
      this.errorHandler.handle(response.json());
    }
  }
}

export class DotsRepositoryFactory implements RepositoryBuilder<DotStatus, DotParams, ItemRepository<DotStatus, DotParams>> {
  constructor(private url: DotsRepositoryUrl) {}

  public build(): ItemRepository<DotStatus, DotParams> {
    return new DotsRepository(this.url);
  }
}