const API_BASE = "http://localhost:8000";

async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem("access_token");
    const headers = {
        ...(token ? { "Authorization": `Bearer ${token}` } : {}),
        ...options.headers
    };
    if (!(options.body instanceof FormData)) {
        headers["Content-Type"] = "application/json";
    }
    const response = await fetch(API_BASE + endpoint, { ...options, headers });
    if (response.status === 204) return null;
    if (!response.ok) {
        const err = await response.json().catch(() => ({ detail: "Request failed" }));
        throw new Error(err.detail || "Request failed");
    }
    return response.json();
}

function showError(id, msg) {
    const el = document.getElementById(id);
    if (el) { el.textContent = msg; el.style.display = "block"; }
}

function showSuccess(id, msg) {
    const el = document.getElementById(id);
    if (el) { el.textContent = msg; el.style.display = "block"; }
}

function showLoading(id, show) {
    const el = document.getElementById(id);
    if (el) el.style.display = show ? "block" : "none";
}

function requireAuth(requiredRole = null) {
    const token = localStorage.getItem("access_token");
    const role = localStorage.getItem("user_role");
    if (!token) { window.location.href = "/frontend/pages/login.html"; return false; }
    if (requiredRole && role !== requiredRole) { window.location.href = "/frontend/pages/login.html"; return false; }
    return true;
}


class MainApp {
    constructor() {
        console.log("Main app loaded");
    }
}

const mainApp = new MainApp();
// NO loadDashboard here