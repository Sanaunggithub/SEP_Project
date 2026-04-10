class AuthComponent:
    def __init__(self):
        print("Auth component loaded")

    def render_login_form(self):
        """Render login form HTML"""
        return """
        <div class="login-container">
            <h1>Login</h1>
            <div id="auth-error" class="error"></div>
            <div id="auth-success" class="success"></div>
            <div id="auth-loading" class="loading">Loading...</div>
            <form id="login-form">
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit">Login</button>
            </form>
            <div class="auth-links">
                <span>Don't have an account? <a href="register.html">Register here</a></span>
            </div>
        </div>
        """

    def render_register_form(self):
        """Render register form HTML"""
        return """
        <div class="register-container">
            <h1>Register</h1>
            <div id="auth-error" class="error"></div>
            <div id="auth-success" class="success"></div>
            <div id="auth-loading" class="loading">Loading...</div>
            <form id="register-form">
                <div class="form-group">
                    <label for="full_name">Full Name:</label>
                    <input type="text" id="full_name" name="full_name" required>
                </div>
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <div class="form-group">
                    <label for="role">Role:</label>
                    <select id="role" name="role" required>
                        <option value="student">Student</option>
                        <option value="instructor">Instructor</option>
                        <option value="admin">Admin</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="phone_number">Phone Number:</label>
                    <input type="tel" id="phone_number" name="phone_number" required>
                </div>
                <div class="form-group">
                    <label for="date_of_birth">Date of Birth:</label>
                    <input type="date" id="date_of_birth" name="date_of_birth" required>
                </div>
                <div class="form-group">
                    <label for="gender">Gender:</label>
                    <select id="gender" name="gender" required>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="address">Address:</label>
                    <input type="text" id="address" name="address" required>
                </div>
                <div class="form-group">
                    <label for="emergency_contact_name">Emergency Contact Name:</label>
                    <input type="text" id="emergency_contact_name" name="emergency_contact_name" required>
                </div>
                <div class="form-group">
                    <label for="emergency_contact_phone">Emergency Contact Phone:</label>
                    <input type="tel" id="emergency_contact_phone" name="emergency_contact_phone" required>
                </div>
                <button type="submit">Register</button>
            </form>
            <div class="auth-links">
                <span>Already have an account? <a href="login.html">Login here</a></span>
            </div>
        </div>
        """

auth_component = AuthComponent()
