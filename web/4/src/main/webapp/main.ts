import { mount } from 'svelte'
import App from './App.svelte'

const app = document.getElementById('app');
if (!app) {
  throw new Error('App root element was not found');
}

const { currentPageComponent } = (window as any).initialData || {};
const svelteApp = mount(App, {
  target: app,
  props: { currentComponent: currentPageComponent }
})

export default svelteApp