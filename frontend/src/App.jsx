import { Navigate, Route, Routes } from "react-router-dom";
import { Dashboard } from "./pages/Dashboard";
import { Login } from "./pages/Login";
import { Signup } from "./pages/Signup";
import { VerifyEmail } from "./pages/VerifyEmail";

export default function App() {
  return (
    <Routes>
      <Route element={<Dashboard />} path="/" />
      <Route element={<Login />} path="/login" />
      <Route element={<Signup />} path="/signup" />
      <Route element={<VerifyEmail />} path="/verify-email" />
      <Route element={<Navigate replace to="/login" />} path="*" />
    </Routes>
  );
}
