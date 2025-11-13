<style>
  @import '../style.css';
  @import 'style.css';
</style>

<script lang="ts">
  import { AppServices } from '@lib/services';
  import { main as generic_main, handleSubmit } from '../script.js';
  import { main, fillCoords } from './script.js';
  import { DefaultErrorHandler } from '@lib/errors/handler';
  import { onMount } from 'svelte';
  import type { ItemRepository } from '@lib/repository/dot';
  import type { DotParams, DotStatus } from '@lib/dto';
  import plotImage from '@resources/png/plot.png';

  let form: HTMLFormElement;
  let dotsRepository: ItemRepository<DotStatus, DotParams>;
  onMount(() => {
    AppServices.SERVER_ERROR_HANDLER.set(new DefaultErrorHandler(form));
    dotsRepository = AppServices.DOTS_REPOSITORY.get().build();
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

<form class="lab-form" bind:this={form} on:submit|preventDefault={myHandleSubmit}>
  <img src="{plotImage}" on:click={myFillCoords} alt="Dot plot" draggable="false" />
  <div id="dots"></div>
  <input type="hidden" name="X" />
  <input type="hidden" name="Y" />
  <div class="form-field dynamic-slider">
    <p><b>R</b></p>
    <input type="range" name="R" class="wide-input" />
    <p>?</p>
  </div>
  <p class="form-error"></p>
</form>