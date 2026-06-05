import { Route, Routes } from "react-router-dom";

import { MainLayout } from "./layout/MainLayout";
import { HomePage } from "./pages/HomePage";

export function App() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<HomePage />} />
      </Route>
    </Routes>
  );
}
