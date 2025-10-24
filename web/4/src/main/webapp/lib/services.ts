import { getItemContext, setItemContext } from "./repository/dots.js";

export const AppServices = {
  DOTS_REPOSITORY: {
    get: getItemContext,
    set: setItemContext,
  },
} as const;