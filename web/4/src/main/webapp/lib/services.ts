import { getServerErrorHandler, setServerErrorHandler } from "./errors/handler.js";
import { getItemContext, setItemContext } from "./repository/dots.js";

export const AppServices = {
  DOTS_REPOSITORY: {
    get: getItemContext,
    set: setItemContext,
  },
  SERVER_ERROR_HANDLER: {
    get: getServerErrorHandler,
    set: setServerErrorHandler,
  }
} as const;