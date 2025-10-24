<style>
  @import '../style.css';
  @import 'style.css';
</style>

<script lang="ts">
  import { AppServices } from 'lib/services.js';
  import { handleSubmit } from '../script.js';

  const dotsRepository = AppServices.DOTS_REPOSITORY.get();

  function myHandleSubmit(event: Event) {
    handleSubmit(event, dotsRepository);
  }
</script>

<form class="lab-form" on:submit|preventDefault={handleSubmit}>
  <img src="/resources/png/plot.png" alt="Dot plot" draggable="false" />
  <div id="dots"></div>
  <div class="form-field">
    <p><b>R</b></p>
    <input type="range" class="wide-input" />
    <p>?</p>
  </div>
  <p class="form-error"></p>
</form>