<style>
  @import 'style.css';
</style>

<script lang="ts">
  import type { NodeDot } from "@lib/dto";
  import { AppServices } from "@lib/services";

  const dotsRepository = AppServices.DOTS_REPOSITORY.get().build();
  let dots: NodeDot[] = dotsRepository.getCache();
</script>

<table class="query-history">
  <caption>
    <b>История запросов</b>
  </caption>
  <thead>
    <tr class="header-row"><td>X</td><td>Y</td><td>R</td><td>Итог</td><td>Дата</td><td>Пользователь</td></tr>
  </thead>
  <tbody class="query-history-body">
    {#if dots.length === 0}
    <tr>
      <td colspan="100">Нет запросов!</td>
    </tr>
    {/if}
    {#each dots as node}
      <tr>
        <td>{node.value.dot.X}</td><td>{node.value.dot.Y}</td><td>{node.value.dot.R}</td><td>{node.value.hit ? "да" : "нет"}</td><td>{node.value.date}</td><td>{node.key}</td>
      </tr>
    {/each}
  </tbody>
</table>