<style>
  @import url('@styles/lab-body.css');
  @import url('@styles/groups.css');
</style>

<script>
  import HeaderComponent from '@components/header/HeaderComponent.svelte';
  import LoginFormComponent from '@components/forms/login-form/LoginFormComponent.svelte';
  import { AppServices } from '@lib/services';
  import { UsersRepositoryFactory } from '@lib/repository/user';
  import { AUTH_URLS } from '@scripts/app';

  AppServices.USERS_REPOSITORY.set(new UsersRepositoryFactory(AUTH_URLS));
</script>

<div class="lab-body">
  <HeaderComponent />
  <div class="form-wrap">
    <LoginFormComponent />
  </div>
</div>