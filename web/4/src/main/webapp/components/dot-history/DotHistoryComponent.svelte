<style>
  @import 'style.css';
</style>

<script lang="ts">
  import type { DotStatus } from "@lib/dto";
  import { AppServices } from "@lib/services";

  const dotsRepository = AppServices.DOTS_REPOSITORY.get().build();
  let dots: DotStatus[] = dotsRepository.getCache();
</script>

<table class="query-history">
  <caption>
    <b>История запросов</b>
  </caption>
  <thead>
    <tr class="header-row"><td>X</td><td>Y</td><td>R</td><td>Результат</td><td>Дата</td></tr>
  </thead>
  <tbody class="query-history-body">
    {#if dots.length === 0}
    <tr>
      <td colspan="100">Нет запросов!</td>
    </tr>
    {/if}
    {#each dots as dot}
      <tr>
        <td>{dot.dot.X}</td><td>{dot.dot.Y}</td><td>{dot.dot.R}</td><td>{dot.hit ? "да" : "нет"}</td><td>{dot.date}</td>
      </tr>
    {/each}
  </tbody>
</table>