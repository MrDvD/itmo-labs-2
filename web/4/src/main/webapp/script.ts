import { mount } from 'svelte'
import MainPage from '@components/pages/main/MainPage.svelte';
import DotsPage from '@components/pages/dots/DotsPage.svelte';
import { APP_ROUTES } from '@scripts/app.js';

function main() {
  const app = document.getElementById('app');
  if (!app) {
    throw new Error('App root element was not found');
  }

  const routes = {
    [APP_ROUTES.ROOT]: {
      title: "Start",
      page: MainPage,
    },
    [APP_ROUTES.DOTS]: {
      title: "Main",
      page: DotsPage,
    }
  };

  const currentPath = window.location.pathname;
  let currentPageComponent;
  if (currentPath in routes) {
    currentPageComponent = routes[currentPath as keyof typeof routes];
  } else {
    window.location.replace("/");
  }

  if (currentPageComponent === undefined) {
    throw new Error(`No component found for path: ${currentPath}`);
  }

  document.title = currentPageComponent.title;
  mount(currentPageComponent.page, {
    target: app,
  });
}

main();