import type { NewUser } from "@lib/dto.js";
import type { AuthRepository } from "@lib/repository/user.js";
import { CLIENT_STATE } from "@scripts/stores.js";

export function exitUser(usersRepository: AuthRepository<unknown, NewUser>): void {
  usersRepository.exit()
  .then(() => {
    CLIENT_STATE.set({ isAuthorized: false });
    window.location.assign("/");
  })
  .catch((err) => {
    if (err) {
      console.error("Error during exiting:", err);
    }
  })
}