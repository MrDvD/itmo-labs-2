<style>
  @import url('@styles/lab-body.less');
  @import url('@styles/groups.less');
  @import url('@styles/pages.css');
</style>

<script>
  import HeaderComponent from '@components/header/HeaderComponent.svelte';
  import LoginFormComponent from '@components/forms/login-form/LoginFormComponent.svelte';
  import { AppServices } from '@lib/services';
  import { UsersRepositoryFactory } from '@lib/repository/user';
  import { AUTH_URLS } from '@scripts/app';
  import { DefaultErrorHandler } from '@lib/errors/handler';

  AppServices.SERVER_ERROR_HANDLER.set(new DefaultErrorHandler(document.documentElement));
  AppServices.USERS_REPOSITORY.set(new UsersRepositoryFactory(AUTH_URLS));
</script>

<div class="lab-body">
  <div class="bar">
    <HeaderComponent />
  </div>
  <div class="form-wrap body margin-all">
    <LoginFormComponent />
  </div>
</div>