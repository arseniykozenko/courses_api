import { Route, Routes } from "react-router-dom"
import Products from "./components/Products.jsx"
import NotFoundPage from "./components/NotFoundPage.jsx"
import { appRoutes } from "./router/routes.js";

const AppRouter = () => {
  return (
      <Routes>
        {appRoutes.map(route => 
            <Route
                Component={route.component}
                path={route.path}
                key={route.path}
            />
        )}
        <Route path="/" element={<Products />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
  );
};

export default AppRouter;