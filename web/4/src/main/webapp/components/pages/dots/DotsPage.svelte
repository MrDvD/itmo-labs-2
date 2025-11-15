<style>
  @import url('@styles/lab-body.css');
  @import url('@styles/groups.css');
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
  import { exitUser } from './script';
  import type { DotStatus } from '@lib/dto';

  AppServices.SERVER_ERROR_HANDLER.set(new DefaultErrorHandler(document.documentElement));

  const dots = $state<DotStatus[]>([]);
  const dotsRepositoryFactory = new DotsRepositoryFactory(DOTS_URLS, dots);
  const dotsRepository = dotsRepositoryFactory.build();
  dotsRepository.get();

  AppServices.DOTS_REPOSITORY.set(dotsRepositoryFactory);
  const usersRepositoryFactory = new UsersRepositoryFactory(AUTH_URLS)
  const usersRepository = usersRepositoryFactory.build();
  AppServices.USERS_REPOSITORY.set(usersRepositoryFactory);

  function myExitUser() {
    exitUser(usersRepository);
  }
</script>

<div class="lab-body">
  <HeaderComponent />

  <button onclick={myExitUser}>Выйти</button>

  <div class="form-wrap">
    <div class="horizontal-group">
      <DotFormComponent />
      <PlotFormComponent />
    </div>
  </div>
  <DotHistoryComponent />
</div>