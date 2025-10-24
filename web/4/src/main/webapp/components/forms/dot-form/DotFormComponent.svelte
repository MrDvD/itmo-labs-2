<style>
  @import '../style.css';
</style>

<script lang="ts">
  import { AppServices } from 'lib/services.js';
  import { handleSubmit } from '../script.js';
  import { handleClean } from './script.js';

  const dotsRepository = AppServices.DOTS_REPOSITORY.get();

  function myHandleSubmit(event: Event) {
    handleSubmit(event, dotsRepository);
  }

  function myHandleClean(event: Event) {
    handleClean(event, dotsRepository);
  }
</script>

<form class='lab-form' on:submit|preventDefault={myHandleSubmit}>
  <p>Проверка точки</p>
  <div class="form-field">
    <p><b>X</b></p>
    <input type="text" class="wide-input" placeholder="Введите дробное число" />
  </div>
  <p class="form-error"></p>
  <div class="form-field">
    <p><b>Y</b></p>
    <input type="text" class="wide-input" placeholder="Введите дробное число" />
  </div>
  <p class="form-error"></p>
  <div class="form-field">
    <p><b>R</b></p>
    <input type="text" class="wide-input" placeholder="Введите дробное число" />
  </div>
  <p class="form-error"></p>
  <button type="submit">Отправить</button>
  <button type="button" on:click={myHandleClean}>Очистить</button>
</form>