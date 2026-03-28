class AuthManager {
    constructor() {
        this.registerForm = document.getElementById('register-form');
        this.loginForm = document.getElementById('login-form');
        this.registerForm.addEventListener('submit', this.register.bind(this));
        this.loginForm.addEventListener('submit', this.login.bind(this));
    }

    async register(e) {
        e.preventDefault();
        const data = { username: document.getElementById('username').value, password: document.getElementById('password').value };
        await fetch('http://localhost:8000/auth/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
        alert('Registered');
    }

    async login(e) {
        e.preventDefault();
        const data = { username: document.getElementById('login-username').value, password: document.getElementById('login-password').value };
        const response = await fetch('http://localhost:8000/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
        if (response.ok) alert('Logged in');
        else alert('Failed');
    }
}

const authManager = new AuthManager();
