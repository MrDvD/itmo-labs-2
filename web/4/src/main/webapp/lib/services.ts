import { getServerErrorHandler, setServerErrorHandler } from "@lib/errors/handler.js";
import { getItemContext, setItemContext } from "@lib/repository/dots.js";

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