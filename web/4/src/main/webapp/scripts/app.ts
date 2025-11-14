import type { DotsRepositoryUrl } from "@lib/repository/dot.js";
import type { UsersRepositoryUrl } from "@lib/repository/user.js";

export const DOTS_URLS: DotsRepositoryUrl = {
  get: "/api/1/dots/",
  post: "/api/1/dots/",
  delete: "/api/1/dots/",
};

export const AUTH_URLS: UsersRepositoryUrl = {
  login: "/api/1/login/",
  register: "/api/1/register/",
  exit: "/api/1/exit/",
};

export const APP_ROUTES = {
  ROOT: "/",
  DOTS: "/dots/"
}