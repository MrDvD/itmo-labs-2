<style>
  @import '../style.css';
  @import 'style.css';
</style>

<script lang="ts">
  import { AppServices } from 'lib/services.js';
  import { main as generic_main, handleSubmit } from '../script.js';
  import { main } from './script.js';

  generic_main();
  main();

  const dotsRepository = AppServices.DOTS_REPOSITORY.get();

  function myHandleSubmit(event: Event) {
    handleSubmit(event, dotsRepository);
  }
</script>

<form class="lab-form" on:submit|preventDefault={myHandleSubmit}>
  <img src="/resources/png/plot.png" alt="Dot plot" draggable="false" />
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