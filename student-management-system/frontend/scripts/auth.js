// ─── Login ───────────────────────────────────────────────────────────────────
async function loginUser(email, password) {
    try {
        showLoading("auth-loading", true);
        showError("auth-error", "");

        const response = await fetch(`${API_BASE}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({ username: email, password })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Login failed");
        }

        const data = await response.json();
        console.log("Login response:", data);

        if (!data.access_token || !data.user) {
            throw new Error("Unexpected response from server");
        }
        
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("user_role", data.user.role);
        localStorage.setItem("user_id", data.user.id);

        // For student: use /students/me or /students/by-user/{id} instead of
        // fetching ALL students (which is admin-only and causes 401)
        if (data.user.role === "student") {
            try {
                // Use the token we just received directly in this call
                const studentRes = await fetch(`${API_BASE}/students/by-user/${data.user.id}`, {
                    headers: { "Authorization": `Bearer ${data.access_token}` }
                });
                if (studentRes.ok) {
                    const student = await studentRes.json();
                    localStorage.setItem("student_id", student.id);
                }
            } catch (err) {
                console.warn("Could not fetch student_id:", err);
                // Non-fatal — continue to redirect
            }
        }

        const redirectMap = {
            "admin": "admin/dashboard.html",
            "instructor": "dashboard.html",
            "student": "student/dashboard.html"
        };
        window.location.href = redirectMap[data.user.role] || "login.html";

    } catch (err) {
        showError("auth-error", err.message);
    } finally {
        showLoading("auth-loading", false);
    }
}

// ─── Register ─────────────────────────────────────────────────────────────────
async function registerUser(fullName, email, password, role, phoneNumber, dateOfBirth, gender, address, emergencyContactName, emergencyContactPhone) {
    try {
        showLoading("auth-loading", true);
        showError("auth-error", "");

        // apiFetch handles Content-Type: application/json automatically
        // Pass a plain object — NOT a pre-stringified string
        await apiFetch("/auth/register", {
            method: "POST",
            body: JSON.stringify({
                full_name: fullName,
                email: email,
                password: password,
                role: role || "student",
                phone_number: phoneNumber,
                date_of_birth: dateOfBirth,
                gender: gender,
                address: address,
                emergency_contact_name: emergencyContactName,
                emergency_contact_phone: emergencyContactPhone
            })
        });

        showSuccess("auth-success", "Registration successful! Redirecting to login...");
        setTimeout(() => { window.location.href = "/pages/login.html"; }, 2000);

    } catch (err) {
        showError("auth-error", err.message);
    } finally {
        showLoading("auth-loading", false);
    }
}

// ─── Logout ───────────────────────────────────────────────────────────────────
async function logoutUser() {
    try {
        await apiFetch("/auth/logout", { method: "POST" });
    } catch (err) {
        console.error("Logout error:", err);
    } finally {
        localStorage.clear();
        window.location.href = "/frontend/pages/login.html";
    }
}

// ─── Get current user ─────────────────────────────────────────────────────────
async function getMe() {
    try {
        return await apiFetch("/auth/me");
    } catch (err) {
        console.error("Get user error:", err);
        throw err;
    }
}

// ─── Update profile ───────────────────────────────────────────────────────────
async function updateProfile(fullName, profilePictureUrl, phoneNumber, address, emergencyContactName, emergencyContactPhone) {
    try {
        const updates = {};
        if (fullName !== undefined) updates.full_name = fullName;
        if (profilePictureUrl !== undefined) updates.profile_picture_url = profilePictureUrl;
        if (phoneNumber !== undefined) updates.phone_number = phoneNumber;
        if (address !== undefined) updates.address = address;
        if (emergencyContactName !== undefined) updates.emergency_contact_name = emergencyContactName;
        if (emergencyContactPhone !== undefined) updates.emergency_contact_phone = emergencyContactPhone;

        return await apiFetch("/auth/me", {
            method: "PUT",
            body: JSON.stringify(updates)
        });
    } catch (err) {
        console.error("Update profile error:", err);
        throw err;
    }
}