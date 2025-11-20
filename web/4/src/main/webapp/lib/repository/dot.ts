import { NodeDotSchema, PageSchema, type DotParams, type NodeDot, type Page } from "@lib/dto.js";
import { AppServices } from "@lib/services.js";
import { createContext } from "svelte";
import type { ReactiveRepository, Repository, RepositoryBuilder } from "./util.js";

export interface ItemRepository<Item, Params> extends Repository<Item, Params> {
  get(pageNumber: number): Promise<Page>;
  post(data: Params): Promise<Item>;
  delete(login: string): Promise<void>;
};

export interface ReactiveItemRepository<Item, Params> extends ItemRepository<Item, Params>, ReactiveRepository<Item, Params, Page> {}

export interface DotsRepositoryUrl {
  get: string;
  post: string;
  delete: string;
}

export const [ getItemContext, setItemContext ] = createContext<RepositoryBuilder<NodeDot, DotParams, ReactiveItemRepository<NodeDot, DotParams>>>();

export class DotsRepository implements ItemRepository<NodeDot, DotParams> {
  private errorHandler = AppServices.SERVER_ERROR_HANDLER.get();

  constructor(private url: DotsRepositoryUrl) {}

  public async get(pageNumber: number): Promise<Page> {
    const response = await fetch(this.url.get + `?page=${pageNumber}`, {
      method: "GET",
      credentials: "include",
    });
    if (!response.ok) {
      this.errorHandler.handle(await response.json());
      return Promise.reject();
    }
    const result = PageSchema.safeParse(await response.json());
    if (result.success) {
      return result.data;
    } else {
      return Promise.reject();
    }
  }
  public async post(data: DotParams): Promise<NodeDot> {
    const response = await fetch(this.url.post, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      this.errorHandler.handle(await response.json());
      return Promise.reject();
    }
    const result = NodeDotSchema.safeParse(await response.json());
    if (result.success) {
      return result.data;
    }
    return Promise.reject();
  }
  public async delete(_: string): Promise<void> {
    const response = await fetch(this.url.delete, {
      method: "DELETE",
      credentials: "include",
    });
    if (!response.ok) {
      this.errorHandler.handle(await response.json());
      return Promise.reject();
    }
  }
}

export class ReactiveDotsRepository implements ReactiveItemRepository<NodeDot, DotParams> {
  constructor(private repository: ItemRepository<NodeDot, DotParams>, private page: Page) {}

  public getCache(): Page {
    return this.page;
  }

  public async get(pageNumber: number): Promise<Page> {
    const response = await this.repository.get(pageNumber);
    this.page.items.length = 0
    this.page.items.push(...response.items);
    this.page.pageNumber = response.pageNumber;
    this.page.pageSize = response.pageSize;
    this.page.totalItems = response.totalItems;
    this.page.totalPages = response.totalPages;
    return this.page;
  }

  public async post(data: DotParams): Promise<NodeDot> {
    const response = await this.repository.post(data);
    await this.get(this.page.pageNumber);
    return response;
  }

  public async delete(login: string): Promise<void> {
    try {
      await this.repository.delete(login);
      await this.get(0);
    } catch (err) {
      console.error("Can't delete dots:", err);
    }
  }
}

export class DotsRepositoryFactory implements RepositoryBuilder<NodeDot, DotParams, ReactiveItemRepository<NodeDot, DotParams>> {
  constructor(private url: DotsRepositoryUrl, private page: Page) {}

  public build(): ReactiveItemRepository<NodeDot, DotParams> {
    return new ReactiveDotsRepository(new DotsRepository(this.url), this.page);
  }
}