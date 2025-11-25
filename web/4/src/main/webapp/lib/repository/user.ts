import { ClientStateSchema, type ClientState, type NewUser } from "@lib/dto.js";
import { AppServices } from "@lib/services.js";
import { createContext } from "svelte";
import type { Repository, RepositoryBuilder } from "./util.js";

export interface AuthRepository<Item, Creds> extends Repository<Item, Creds> {
  login(id: Creds): Promise<Item>;
  register(data: Creds): Promise<Item>;
  exit(): Promise<void>;
};

export const [ getUserContext, setUserContext ] = createContext<RepositoryBuilder<ClientState, NewUser, AuthRepository<ClientState, NewUser>>>();

export interface UsersRepositoryUrl {
  login: string;
  register: string;
  exit: string;
}

export class UsersRepository implements AuthRepository<ClientState, NewUser> {
  private errorHandler = AppServices.SERVER_ERROR_HANDLER.get();

  constructor(private url: UsersRepositoryUrl) {}

  public async login(user: NewUser): Promise<ClientState> {
    const response = await fetch(this.url.login, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(user),
    });
    if (!response.ok) {
      this.errorHandler.handle(response.json());
      return Promise.reject();
    }
    const rawState = await response.json();
    const result = ClientStateSchema.safeParse(rawState);
    if (result.success) {
      return result.data;
    }
    return Promise.reject();
  }
  public async register(user: NewUser): Promise<ClientState> {
    const response = await fetch(this.url.register, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(user),
    });
    if (!response.ok) {
      this.errorHandler.handle(response.json());
      return Promise.reject();
    }
    const rawState = await response.json();
    const result = ClientStateSchema.safeParse(rawState);
    if (result.success) {
      return result.data;
    }
    return Promise.reject();
  }
  public async exit(): Promise<void> {
    const response = await fetch(this.url.exit, {
      method: "HEAD",
    });
    if (!response.ok) {
      this.errorHandler.handle(response.json());
      return Promise.reject();
    }
  }
}

export class UsersRepositoryFactory implements RepositoryBuilder<ClientState, NewUser, AuthRepository<ClientState, NewUser>> {
  constructor(private url: UsersRepositoryUrl) {}

  public build(): AuthRepository<ClientState, NewUser> {
    return new UsersRepository(this.url);
  }
}