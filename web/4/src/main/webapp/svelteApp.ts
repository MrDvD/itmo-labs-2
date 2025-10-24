import { mount } from 'svelte'

const app = document.getElementById('app');
if (!app) {
  throw new Error('App root element was not found');
}

const { currentPageComponent } = (window as any).initialData || {};
const svelteApp = mount(currentPageComponent, {
  target: app,
});

export default svelteApp