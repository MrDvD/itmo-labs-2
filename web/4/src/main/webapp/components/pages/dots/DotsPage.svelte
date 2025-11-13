<style>
  @import url('@styles/lab-body.css');
  @import url('@styles/groups.css');
</style>

<script>
  import HeaderComponent from '@components/header/HeaderComponent.svelte';
  import DotFormComponent from '@components/forms/dot-form/DotFormComponent.svelte';
  import PlotFormComponent from '@components/forms/plot-form/PlotFormComponent.svelte';
  import DotHistoryComponent from '@components/dot-history/DotHistoryComponent.svelte';
  import { DotsRepositoryFactory } from '@lib/repository/dot';
  import { AppServices } from '@lib/services';
  import { AUTH_URLS, DOTS_URLS } from '@scripts/app';
  import { UsersRepositoryFactory } from '@lib/repository/user';
  import { DefaultErrorHandler } from '@lib/errors/handler';

  AppServices.SERVER_ERROR_HANDLER.set(new DefaultErrorHandler(Document));
  AppServices.DOTS_REPOSITORY.set(new DotsRepositoryFactory(DOTS_URLS));
  AppServices.USERS_REPOSITORY.set(new UsersRepositoryFactory(AUTH_URLS));
</script>

<div class="lab-body">
  <HeaderComponent />

  <a href="/">Назад</a>

  <div class="form-wrap">
    <div class="horizontal-group">
      <DotFormComponent />
      <PlotFormComponent />
    </div>
  </div>
  <DotHistoryComponent />
</div>