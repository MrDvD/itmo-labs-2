<style>
  @import '../style.css';
  @import 'style.css';
</style>

<script lang="ts">
  import { AppServices } from '@lib/services';
  import { main as generic_main, handleSubmit } from '../script.js';
  import { main, fillCoords, getScale } from './script.js';
  import { DefaultErrorHandler } from '@lib/errors/handler';
  import { onMount } from 'svelte';
  import type { ReactiveItemRepository } from '@lib/repository/dot.js';
  import type { DotParams, DotStatus } from '@lib/dto';
  import plotImage from '@resources/png/plot.png';

  let form: HTMLFormElement;
  let dotsRepository: ReactiveItemRepository<DotStatus, DotParams>;
  let dots: DotStatus[];
  let img: HTMLImageElement;
  onMount(() => {
    AppServices.SERVER_ERROR_HANDLER.set(new DefaultErrorHandler(form));
    dotsRepository = AppServices.DOTS_REPOSITORY.get().build();
    dots = dotsRepository.getCache();
  });
  generic_main();
  main();

  function myHandleSubmit(event: Event) {
    handleSubmit(event, dotsRepository);
  }

  function myFillCoords(event: MouseEvent) {
    fillCoords(form, event);
  }
</script>

<form class="lab-form" bind:this={form} onsubmit={myHandleSubmit}>
  <div class="dots-container">
    <img src="{plotImage}" bind:this={img} onclick={myFillCoords} alt="Dot plot" draggable="false" />
    {#each dots as dot}
      <div class={["dot", dot.hit ? 'correct' : 'wrong']} style:transform="translate({dot.dot.X * getScale(img) / dot.dot.R}px, {-dot.dot.Y * getScale(img) / dot.dot.R}px)"></div>
    {/each}
  </div>
  <input type="hidden" name="X" />
  <input type="hidden" name="Y" />
  <div class="form-field dynamic-slider">
    <p><b>R</b></p>
    <input type="range" name="R" class="wide-input" />
    <p>?</p>
  </div>
  <p class="form-error"></p>
</form>