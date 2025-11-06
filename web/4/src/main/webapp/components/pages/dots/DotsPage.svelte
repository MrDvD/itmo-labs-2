<style>
  @import '../lab-body.css';
  @import 'style.css';
</style>

<script>
  import HeaderComponent from '/components/header/HeaderComponent.svelte';
  import DotFormComponent from '/components/forms/dot-form/DotFormComponent.svelte';
  import PlotFormComponent from '/components/forms/plot-form/PlotFormComponent.svelte';
  import DotHistoryComponent from '/components/dot-history/DotHistoryComponent.svelte';
  import { DefaultDotsRepository } from 'lib/repository/dots.js';
  import { AppServices } from 'lib/services.js';

  AppServices.DOTS_REPOSITORY.set(DefaultDotsRepository());
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