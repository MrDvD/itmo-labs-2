import { getServerErrorHandler, setServerErrorHandler } from "@lib/errors/handler.js";
import { getItemContext, setItemContext } from "@lib/repository/dot.js";
import { getUserContext, setUserContext } from "./repository/user.js";

export const AppServices = {
  DOTS_REPOSITORY: {
    get: getItemContext,
    set: setItemContext,
  },
  USERS_REPOSITORY: {
    get: getUserContext,
    set: setUserContext,
  },
  SERVER_ERROR_HANDLER: {
    get: getServerErrorHandler,
    set: setServerErrorHandler,
  },
} as const;