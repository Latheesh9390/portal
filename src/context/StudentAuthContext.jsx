import { createContext, useContext, useState } from "react";
import { studentLogin, studentRegister } from "../api/studentApi";

const StudentAuthContext = createContext(null);

export function StudentAuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("student_token"));
  const [hallticket, setHallticket] = useState(() => localStorage.getItem("student_hallticket"));
  const [name, setName] = useState(() => localStorage.getItem("student_name"));

  function _persist(data) {
    localStorage.setItem("student_token", data.access_token);
    localStorage.setItem("student_hallticket", data.username);
    if (data.name) localStorage.setItem("student_name", data.name);
    setToken(data.access_token);
    setHallticket(data.username);
    setName(data.name || null);
  }

  async function login(credentials) {
    const data = await studentLogin(credentials);
    _persist(data);
  }

  async function register(details) {
    // Registration logs the new student straight in, same as login() does.
    const data = await studentRegister(details);
    _persist(data);
  }

  function logout() {
    localStorage.removeItem("student_token");
    localStorage.removeItem("student_hallticket");
    localStorage.removeItem("student_name");
    setToken(null);
    setHallticket(null);
    setName(null);
  }

  const value = {
    token,
    hallticket,
    name,
    isAuthenticated: Boolean(token),
    login,
    register,
    logout,
  };

  return <StudentAuthContext.Provider value={value}>{children}</StudentAuthContext.Provider>;
}

export function useStudentAuth() {
  const ctx = useContext(StudentAuthContext);
  if (!ctx) {
    throw new Error("useStudentAuth must be used inside a StudentAuthProvider");
  }
  return ctx;
}
