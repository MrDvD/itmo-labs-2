import { DotStatusSchema, type DotParams, type DotStatus } from "@lib/dto.js";
import { AppServices } from "@lib/services.js";
import { createContext } from "svelte";
import type { ReactiveRepository, Repository, RepositoryBuilder } from "./util.js";

export interface ItemRepository<Item, Params> extends Repository<Item, Params> {
  get(): Promise<Item[]>;
  post(data: Params): Promise<Item>;
  delete(): Promise<void>;
};

export interface ReactiveItemRepository<Item, Params> extends ItemRepository<Item, Params>, ReactiveRepository<Item, Params> {}

export interface DotsRepositoryUrl {
  get: string;
  post: string;
  delete: string;
}

export const [ getItemContext, setItemContext ] = createContext<RepositoryBuilder<DotStatus, DotParams, ReactiveItemRepository<DotStatus, DotParams>>>();

export class DotsRepository implements ItemRepository<DotStatus, DotParams> {
  private errorHandler = AppServices.SERVER_ERROR_HANDLER.get();

  constructor(private url: DotsRepositoryUrl) {}

  public async get(): Promise<DotStatus[]> {
    const response = await fetch(this.url.get, {
      method: "GET",
      credentials: "include",
    });
    if (!response.ok) {
      this.errorHandler.handle(response.json());
      return Promise.reject();
    }
    const results: DotStatus[] = [];
    const rawResult = await response.json();
    if (rawResult && Array.isArray(rawResult)) {
      for (const item of rawResult) {
        const result = DotStatusSchema.safeParse(item);
        if (result.success) {
          results.push(result.data);
        } else {
          return Promise.reject();
        }
      }
    } else {
      return Promise.reject();
    }
    return results;
  }
  public async post(data: DotParams): Promise<DotStatus> {
    const response = await fetch(this.url.post, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      this.errorHandler.handle(response.json());
      return Promise.reject();
    }
    const rawResult = await response.json();
    const result = DotStatusSchema.safeParse(rawResult);
    if (result.success) {
      return result.data;
    }
    return Promise.reject();
  }
  public async delete(): Promise<void> {
    const response = await fetch(this.url.delete, {
      method: "DELETE",
      credentials: "include",
    });
    if (!response.ok) {
      this.errorHandler.handle(response.json());
      return Promise.reject();
    }
  }
}

export class ReactiveDotsRepository implements ReactiveItemRepository<DotStatus, DotParams> {
  constructor(private repository: ItemRepository<DotStatus, DotParams>, private dots: DotStatus[]) {}

  public getCache(): DotStatus[] {
    return this.dots;
  }

  public async get(): Promise<DotStatus[]> {
    const response = await this.repository.get();
    this.dots.length = 0;
    this.dots.push(...response);
    return this.dots;
  }

  public async post(data: DotParams): Promise<DotStatus> {
    const response = await this.repository.post(data);
    this.dots.push(response);
    return response;
  }

  public async delete(): Promise<void> {
    await this.repository.delete();
    this.dots.length = 0;
  }
}

export class DotsRepositoryFactory implements RepositoryBuilder<DotStatus, DotParams, ReactiveItemRepository<DotStatus, DotParams>> {
  constructor(private url: DotsRepositoryUrl, private dots: DotStatus[]) {}

  public build(): ReactiveItemRepository<DotStatus, DotParams> {
    return new ReactiveDotsRepository(new DotsRepository(this.url), this.dots);
  }
}