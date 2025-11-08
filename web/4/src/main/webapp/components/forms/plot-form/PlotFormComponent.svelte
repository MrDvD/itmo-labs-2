<style>
  @import '../style.css';
  @import 'style.css';
</style>

<script lang="ts">
  import { AppServices } from 'lib/services.js';
  import { main as generic_main, handleSubmit } from '../script.js';
  import { main, fillCoords } from './script.js';

  generic_main();
  main();

  const dotsRepository = AppServices.DOTS_REPOSITORY.get();
  let form;

  function myHandleSubmit(event: Event) {
    handleSubmit(event, dotsRepository);
  }

  function myFillCoords(event: MouseEvent) {
    fillCoords(form, event);
  }
</script>

<form class="lab-form" bind:this={form} on:submit|preventDefault={myHandleSubmit}>
  <img src="/resources/png/plot.png" on:click={myFillCoords} alt="Dot plot" draggable="false" />
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