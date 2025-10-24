import type { DotParams, DotStatus } from "lib/dto.js";
import type { ItemRepository } from "lib/repository/dots.js";

export async function handleClean(event: Event, dotsRepository: ItemRepository<DotStatus, DotParams>): Promise<void> {
  event.preventDefault();
  await dotsRepository.delete();
}