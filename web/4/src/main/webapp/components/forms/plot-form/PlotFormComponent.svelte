<style>
  @import '../style.css';
  @import 'style.css';
</style>

<script lang="ts">
  import { AppServices } from '@lib/services';
  import { handleSubmit, initQueryStatus, initValidation } from '../script.js';
  import { fillCoords, getScale } from './script.js';
  import { DefaultErrorHandler } from '@lib/errors/handler';
  import { onMount } from 'svelte';
  import type { ReactiveItemRepository } from '@lib/repository/dot.js';
  import type { DotParams, DotStatus } from '@lib/dto';
  import plotImage from '@resources/png/plot.png';
  import { writable } from 'svelte/store';

  let form: HTMLFormElement;
  let dotsRepository: ReactiveItemRepository<DotStatus, DotParams>;
  let dots = writable<DotStatus[]>([]);
  let img = writable<HTMLImageElement>();
  let queryError: Element;
  let R: number = $state(1);
  let imageScale = $derived(() => {
    if (!$img) return 1;
    return getScale($img) / R;
  });
  onMount(() => {
    AppServices.SERVER_ERROR_HANDLER.set(new DefaultErrorHandler(form));
    dotsRepository = AppServices.DOTS_REPOSITORY.get().build();
    dots.set(dotsRepository.getCache());
    initValidation(form);
    initQueryStatus(form, queryError);
  });

  function myHandleSubmit(event: Event) {
    handleSubmit(event, dotsRepository);
  }

  function myFillCoords(event: MouseEvent) {
    fillCoords(form, event, R);
  }
</script>

<form class="lab-form" bind:this={form} onsubmit={myHandleSubmit}>
  <div class="dots-container">
    <img src="{plotImage}" bind:this={$img} onclick={myFillCoords} alt="Dot plot" draggable="false" />
    {#each $dots as dot}
      {#if Math.max(Math.abs(dot.dot.X), Math.abs(dot.dot.Y)) <= R}
        <div class={["dot", dot.hit ? 'correct' : 'wrong']} style:transform="translate({dot.dot.X * imageScale()}px, {-dot.dot.Y * imageScale()}px)"></div>
      {/if}
    {/each}
  </div>
  <input type="hidden" name="X" />
  <input type="hidden" name="Y" />
  <div class="form-field dynamic-slider">
    <p><b>R</b></p>
    <input type="range" name="R" class="wide-input" min="0.2" max="3" step="0.1" bind:value={R} />
    <p>{R}</p>
  </div>
  <p class="form-error"></p>
  <p bind:this={queryError} class="form-error"></p>
</form>