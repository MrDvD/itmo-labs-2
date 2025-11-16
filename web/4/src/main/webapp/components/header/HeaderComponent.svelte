<style>
  @import 'style.css';
</style>

<script lang="ts">
  import { AppServices } from "@lib/services";
  import { exitUser } from "./script";
    import { CLIENT_STATE } from "@scripts/stores";
    import { get } from 'svelte/store';

  const usersRepository = AppServices.USERS_REPOSITORY.get().build();

  function myExitUser() {
    exitUser(usersRepository);
  }
</script>

<header class="lab-header">
  <div>
    Лабин Макар Андреевич<br/>
    P3231
  </div>
  <div>
    <p>Вариант №4466</p>
    {#if get(CLIENT_STATE).isAuthorized }
      <button onclick={myExitUser}>Выйти</button>
    {/if}
  </div>
</header>