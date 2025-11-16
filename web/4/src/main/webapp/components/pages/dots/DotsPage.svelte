<style>
  @import url('@styles/lab-body.less');
  @import url('@styles/groups.less');
  @import url('@styles/pages.css');
  @import url('./style.less');
</style>

<script lang="ts">
  import HeaderComponent from '@components/header/HeaderComponent.svelte';
  import DotFormComponent from '@components/forms/dot-form/DotFormComponent.svelte';
  import PlotFormComponent from '@components/forms/plot-form/PlotFormComponent.svelte';
  import DotHistoryComponent from '@components/dot-history/DotHistoryComponent.svelte';
  import { DotsRepositoryFactory } from '@lib/repository/dot';
  import { AppServices } from '@lib/services';
  import { AUTH_URLS, DOTS_URLS } from '@scripts/app';
  import { UsersRepositoryFactory } from '@lib/repository/user';
  import { DefaultErrorHandler } from '@lib/errors/handler';
  import type { DotStatus } from '@lib/dto';

  AppServices.SERVER_ERROR_HANDLER.set(new DefaultErrorHandler(document.documentElement));

  const dots = $state<DotStatus[]>([]);
  const dotsRepositoryFactory = new DotsRepositoryFactory(DOTS_URLS, dots);
  const dotsRepository = dotsRepositoryFactory.build();
  dotsRepository.get();

  AppServices.DOTS_REPOSITORY.set(dotsRepositoryFactory);
  AppServices.USERS_REPOSITORY.set(new UsersRepositoryFactory(AUTH_URLS));
</script>

<div class="lab-body">
  <div class="bar">
    <HeaderComponent />
  </div>

  <div class="desktop-horizontal-group body">
    <div class="form-wrap desktop-margin">
      <div class="tablet-horizontal-group">
        <DotFormComponent />
        <PlotFormComponent />
      </div>
    </div>
    <div class="history-container">
      <DotHistoryComponent />
    </div>
  </div>
</div>