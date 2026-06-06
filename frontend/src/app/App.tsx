import { Route, Routes } from "react-router-dom";

import { RequireAuth } from "../features/auth/components/RequireAuth";
import { LoginPage } from "../features/auth/pages/LoginPage";
import { RegisterPage } from "../features/auth/pages/RegisterPage";
import { DashboardPage } from "../features/articles/pages/DashboardPage";
import { EditArticlePage } from "../features/articles/pages/EditArticlePage";
import { GenerateArticlePage } from "../features/articles/pages/GenerateArticlePage";
import { MainLayout } from "./layout/MainLayout";

export function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route element={<RequireAuth />}>
        <Route element={<MainLayout />}>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/articles/generate" element={<GenerateArticlePage />} />
          <Route path="/articles/:articleId/edit" element={<EditArticlePage />} />
        </Route>
      </Route>
    </Routes>
  );
}
