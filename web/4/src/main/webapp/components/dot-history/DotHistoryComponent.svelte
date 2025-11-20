<style>
  @import 'style.css';
</style>

<script lang="ts">
    import type { Page } from "@lib/dto";
  import { AppServices } from "@lib/services";

  const dotsRepository = AppServices.DOTS_REPOSITORY.get().build();
  let dotsPage: Page = $state({
    items: [],
    pageNumber: 0,
    pageSize: 0,
    totalItems: 0,
    totalPages: 0,
  });
  $effect(() => {
    dotsRepository.get(dotsPage.pageNumber).then(result => {
      dotsPage = result;
    });
  });
</script>

<table class="query-history">
  <caption>
    <b>История запросов</b>
  </caption>
  <thead>
    <tr class="header-row"><td>X</td><td>Y</td><td>R</td><td>Итог</td><td>Дата</td><td>Пользователь</td></tr>
  </thead>
  <tbody class="query-history-body">
    {#if dotsPage.items.length === 0}
    <tr>
      <td colspan="100">Пустая страница!</td>
    </tr>
    {/if}
    {#each dotsPage.items as node}
      <tr>
        <td>{node.value.dot.X}</td><td>{node.value.dot.Y}</td><td>{node.value.dot.R}</td><td>{node.value.hit ? "да" : "нет"}</td><td>{node.value.date}</td><td>{node.key}</td>
      </tr>
    {/each}
  </tbody>
</table>

<div class="pagination">
  <button disabled={dotsPage.pageNumber === 0} onclick={() => dotsPage.pageNumber--}>Назад</button>
  <span>Страница {dotsPage.pageNumber + 1} из {dotsPage.totalPages}</span>
  <button disabled={dotsPage.pageNumber >= dotsPage.totalPages - 1} onclick={() => dotsPage.pageNumber++}>Вперед</button>
</div>