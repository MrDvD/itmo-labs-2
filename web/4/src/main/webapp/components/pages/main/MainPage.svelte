<style>
  @import url('/styles/lab-body.css');
  @import url('/styles/groups.css');
</style>

<script>
  import HeaderComponent from '/components/header/HeaderComponent.svelte';
  import LoginFormComponent from '/components/forms/login-form/LoginFormComponent.svelte';
</script>

<div class="lab-body">
  <HeaderComponent />
  <a href="/dots/">Redirect</a>
  <div class="form-wrap">
    <LoginFormComponent />
  </div>
</div>