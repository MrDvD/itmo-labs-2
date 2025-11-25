import { mount } from 'svelte'
import MainPage from '@components/pages/main/MainPage.svelte';
import DotsPage from '@components/pages/dots/DotsPage.svelte';
import { APP_ROUTES, COOKIE } from '@scripts/app.js';
import { CLIENT_STATE, getCookie } from '@scripts/stores.js';
import { get } from 'svelte/store';
import { ClientStateSchema } from '@lib/dto.js';

function main() {
  const app = document.getElementById('app');
  if (!app) {
    throw new Error('App root element was not found');
  }

  const rawState = getCookie(COOKIE.CLIENT_STATE);
  if (rawState !== null) {
    const stringState = atob(rawState);
    const parseResult = ClientStateSchema.safeParse(JSON.parse(stringState));
    if (parseResult.success) {
      CLIENT_STATE.set(parseResult.data);
    } else {
      console.warn("Could not restore client state. It was set to default");
    }
  }

  const routes = {
    [APP_ROUTES.ROOT]: {
      title: "Start",
      page: MainPage,
      isAuth: false,
      fallback: APP_ROUTES.DOTS,
    },
    [APP_ROUTES.DOTS]: {
      title: "Main",
      page: DotsPage,
      isAuth: true,
      fallback: APP_ROUTES.ROOT,
    },
  };

  const currentPath = window.location.pathname;
  let currentPage;
  if (currentPath in routes) {
    const route = routes[currentPath as keyof typeof routes] as typeof routes[typeof currentPath];
    if (route.isAuth === get(CLIENT_STATE).isAuthorized) {
      currentPage = route;
    } else {
      window.location.replace(route.fallback);
    }
  } else {
    window.location.replace("/");
  }

  if (currentPage === undefined) {
    throw new Error(`No component found for path: ${currentPath}`);
  }

  document.title = currentPage.title;
  mount(currentPage.page, {
    target: app,
  });
}

main();