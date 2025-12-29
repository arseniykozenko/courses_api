import { Route, Routes } from "react-router-dom"
import Products from "./pages/Products.jsx"
import NotFoundPage from "./pages/NotFoundPage.jsx"
import AuthPage from "./pages/AuthPage.jsx";
import { appRoutes, privateRoutes } from "./router/routes.js";
import { useAuth } from './hooks/UseAuth.js';

const AppRouter = () => {
  const { isAuth } = useAuth();
  return (
    isAuth
    ?
    <Routes>
      {privateRoutes.map(route => 
        <Route
            Component={route.component}
            path={route.path}
            key={route.path}
        />
      )}
      {appRoutes.map(route => 
        <Route
            Component={route.component}
            path={route.path}
            key={route.path}
        />
      )}
    </Routes>
    :
    <Routes>
      {appRoutes.map(route => 
          <Route
              Component={route.component}
              path={route.path}
              key={route.path}
          />
      )}
      <Route path="*" element={<AuthPage />} />
    </Routes>
  );
};

export default AppRouter;