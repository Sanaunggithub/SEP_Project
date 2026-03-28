class NotificationManager {
    constructor() {
        this.form = document.getElementById('notification-form');
        this.list = document.getElementById('notification-list');
        this.form.addEventListener('submit', this.addNotification.bind(this));
        this.loadNotifications();
    }

    async addNotification(e) {
        e.preventDefault();
        const data = { message: document.getElementById('message').value, timestamp: new Date().toISOString() };
        await fetch('http://localhost:8000/notifications/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
        this.loadNotifications();
    }

    async loadNotifications() {
        const response = await fetch('http://localhost:8000/notifications/');
        const notifications = await response.json();
        this.list.innerHTML = notifications.map(n => `<li>${n.message} - ${n.timestamp}</li>`).join('');
    }
}

const notificationManager = new NotificationManager();
