<style>
  @import '../style.css';
</style>

<script lang="ts">
  import { AppServices } from '@lib/services';
  import { handleSubmit, initQueryStatus, initValidation } from '../script.js';
  import { handleClean, initTypeValidation } from './script.js';
  import { DefaultErrorHandler } from '@lib/errors/handler';
  import { onMount } from 'svelte';
  import type { ItemRepository } from '@lib/repository/dot.js';
  import type { DotParams, DotStatus } from '@lib/dto';

  let form: HTMLFormElement;
  let dotsRepository: ItemRepository<DotStatus, DotParams>;
  let queryError: Element;
  onMount(() => {
    AppServices.SERVER_ERROR_HANDLER.set(new DefaultErrorHandler(form));
    dotsRepository = AppServices.DOTS_REPOSITORY.get().build();
    initValidation(form);
    initQueryStatus(form, queryError);
    initTypeValidation(form);
  });

  function myHandleSubmit(event: Event) {
    handleSubmit(event, dotsRepository);
  }

  function myHandleClean(event: Event) {
    handleClean(event, dotsRepository);
  }
</script>

<form class='lab-form' bind:this={form} on:submit|preventDefault={myHandleSubmit}>
  <p>Проверка точки</p>
  <div class="form-field">
    <p><b>X</b></p>
    <input type="text" class="wide-input double-input" name="X" placeholder="Введите дробное число" autocomplete="off" />
  </div>
  <p class="form-error"></p>
  <div class="form-field">
    <p><b>Y</b></p>
    <input type="text" class="wide-input double-input" name="Y" placeholder="Введите дробное число" autocomplete="off" />
  </div>
  <p class="form-error"></p>
  <div class="form-field">
    <p><b>R</b></p>
    <input type="text" class="wide-input double-input" name="R" placeholder="Введите дробное число" autocomplete="off" />
  </div>
  <p class="form-error"></p>
  <button type="submit">Отправить</button>
  <button type="button" on:click={myHandleClean}>Очистить</button>
  <p bind:this={queryError} class="form-error"></p>
</form>