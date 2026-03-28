class AnalyticsManager {
    constructor() {
        this.display = document.getElementById('analytics-display');
        this.loadAnalytics();
    }

    async loadAnalytics() {
        const response = await fetch('http://localhost:8000/analytics/');
        const analytics = await response.json();
        this.display.innerHTML = analytics.map(a => `<p>${a.metric}: ${a.value}</p>`).join('');
    }
}

const analyticsManager = new AnalyticsManager();
