// frontend/src/main.tsx

import React from 'react';
import ReactDOM from 'react-dom/client';
import SuperTokens, { SuperTokensWrapper } from 'supertokens-auth-react';
import Session, { SessionAuth } from 'supertokens-auth-react/recipe/session';
import EmailPassword from 'supertokens-auth-react/recipe/emailpassword';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { MantineProvider } from '@mantine/core';
import { getSuperTokensRoutesForReactRouterDom } from "supertokens-auth-react/ui";
import * as reactRouterDom from 'react-router-dom';
import { EmailPasswordPreBuiltUI } from 'supertokens-auth-react/recipe/emailpassword/prebuiltui';

// --- 1. Supertokens Configuration ---
SuperTokens.init({
  // Retrieve domain information from Vite environment variables
  appInfo: {
    appName: 'KitchenIQ',
    apiDomain: import.meta.env.VITE_APP_API_DOMAIN,
    websiteDomain: import.meta.env.VITE_APP_WEBSITE_DOMAIN,
    apiBasePath: "/auth",
    websiteBasePath: "/auth",
  },
  recipeList: [
    EmailPassword.init(),
    Session.init(),
  ],
});

// --- 2. Root Component ---
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    {/* SuperTokensWrapper is required to manage the session context across the app */}
    <SuperTokensWrapper>
      {/* MantineProvider is required to enable Mantine components */}
      <MantineProvider>
        {/* BrowserRouter is required for Supertokens and our app routing */}
        <BrowserRouter>
          <Routes>
            {getSuperTokensRoutesForReactRouterDom(reactRouterDom, [EmailPasswordPreBuiltUI])}
            <Route path='/' element={<SessionAuth><div>Welcome to KitchenIQ. You are Authenticated.</div></SessionAuth>} />
          </Routes>
        </BrowserRouter>
      </MantineProvider>
    </SuperTokensWrapper>
  </React.StrictMode>,
);