import api from "./axios";

function _unwrap(promise) {
  return promise.then(r => r.data).catch(err => {
    const status = err.response?.status;
    const message = err.response?.data?.detail || "Something went wrong. Please try again.";
    const wrapped = new Error(message);
    wrapped.status = status;
    throw wrapped;
  });
}

// ── Auth (used by StudentAuthContext) ─────────────────────────────────────────

export const studentLogin = (data) => _unwrap(api.post("/api/auth/student/login", data));
export const studentRegister = (data) => _unwrap(api.post("/api/auth/student/register", data));
export const fetchStudentMe = () => _unwrap(api.get("/api/auth/student/me"));

// ── Protected "my results" (no need to type hall ticket again) ───────────────

export const fetchMyResults = (examType = "regular", semester = null) =>
  _unwrap(
    api.get("/api/student/my-results", { params: { exam_type: examType, semester: semester || undefined } })
  );
