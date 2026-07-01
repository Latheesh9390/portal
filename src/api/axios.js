import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

// Two separate account systems (admin dashboard vs. student self-service)
// share this one axios instance. We pick which bearer token to attach based
// on which part of the API the request is going to, so an admin token is
// never sent to a student-only route and vice versa.
api.interceptors.request.use((config) => {
  const url = config.url || "";
  const isStudentRoute = url.startsWith("/api/student") || url.startsWith("/api/auth/student");
  const token = isStudentRoute
    ? localStorage.getItem("student_token")
    : localStorage.getItem("admin_token");

  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default api;
