<!-- <style>
  @import '../style.css';
</style>

<script lang="ts">
  import type { ClientState, NewUser } from "@lib/dto";
  import { DefaultErrorHandler } from "@lib/errors/handler";
  import type { AuthRepository } from "@lib/repository/user";
  import { AppServices } from "@lib/services";
  import { onMount } from "svelte";
  import { handleSubmit } from "./script";
  import { main } from "../script";
  import { APP_ROUTES } from "@scripts/app";

  let form: HTMLFormElement;
  let usersRepository: AuthRepository<ClientState, NewUser>;
  onMount(() => {
    AppServices.SERVER_ERROR_HANDLER.set(new DefaultErrorHandler(form));
    usersRepository = AppServices.USERS_REPOSITORY.get().build();
  });

  main();

  function myHandleSubmit(event: Event) {
    handleSubmit(event, APP_ROUTES.DOTS, usersRepository);
  }
</script>

<form bind:this={form} on:submit={myHandleSubmit} class="lab-form">
  <p>Форма регистрации</p>
  <div class="form-field">
    <p><b>Логин</b></p>
    <input type="text" class="wide-input" name="login" placeholder="Введите логин" />
  </div>
  <p class="form-error"></p>
  <div class="form-field">
    <p><b>Пароль</b></p>
    <input type="password" class="wide-input" name="password" placeholder="Введите пароль" />
  </div>
  <p class="form-error"></p>
  <div class="form-field">
    <p><b>Пароль</b></p>
    <input type="password" class="wide-input" name="password-again" placeholder="Введите пароль повторно" />
  </div>
  <p class="form-error"></p>
  <button type="submit">Зарегистрироваться</button>
</form> -->