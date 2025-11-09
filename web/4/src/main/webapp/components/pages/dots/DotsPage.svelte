<style>
  @import url('/styles/lab-body.css');
  @import url('/styles/groups.css');
</style>

<script>
  import HeaderComponent from '@components/header/HeaderComponent.svelte';
  import DotFormComponent from '@components/forms/dot-form/DotFormComponent.svelte';
  import PlotFormComponent from '@components/forms/plot-form/PlotFormComponent.svelte';
  import DotHistoryComponent from '@components/dot-history/DotHistoryComponent.svelte';
  import { DotsRepositoryFactory } from '@lib/repository/dots.js';
  import { AppServices } from '@lib/services.js';
  import { DefaultErrorHandler } from '@lib/errors/handler.js';

  // AppServices.SERVER_ERROR_HANDLER.set(new DefaultErrorHandler(Document));
  AppServices.DOTS_REPOSITORY.set(new DotsRepositoryFactory());
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