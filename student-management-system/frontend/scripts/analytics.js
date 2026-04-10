class AnalyticsManager {
    constructor() {
        this.display = document.getElementById('analytics-display');
        if (this.display) this.loadAnalytics();
    }

    async loadAnalytics() {
        const response = await fetch('http://localhost:8000/analytics/');
        const analytics = await response.json();
        this.display.innerHTML = analytics.map(a => `<p>${a.metric}: ${a.value}</p>`).join('');
    }
}

const analyticsManager = new AnalyticsManager();

async function getEnrollmentTrends(semester = "", year = "") {
    try {
        let url = "/analytics/enrollment-trends?";
        const params = [];
        if (semester) params.push(`semester=${semester}`);
        if (year) params.push(`year=${year}`);
        url += params.join("&");
        return await apiFetch(url);
    } catch (err) {
        console.error("Get enrollment trends error:", err);
        throw err;
    }
}

async function getAttendancePatterns(courseId = "") {
    try {
        let url = "/analytics/attendance-patterns?";
        if (courseId) url += `course_id=${courseId}`;
        return await apiFetch(url);
    } catch (err) {
        console.error("Get attendance patterns error:", err);
        throw err;
    }
}

async function getGradeDistribution(courseId = "") {
    try {
        let url = "/analytics/grade-distribution?";
        if (courseId) url += `course_id=${courseId}`;
        return await apiFetch(url);
    } catch (err) {
        console.error("Get grade distribution error:", err);
        throw err;
    }
}

async function getStudentPerformance(studentId) {
    try {
        return await apiFetch(`/analytics/student-performance/${studentId}`);
    } catch (err) {
        console.error("Get student performance error:", err);
        throw err;
    }
}

async function generateReport(reportType, parameters = {}, exportFormat = "pdf") {
    try {
        return await apiFetch("/analytics/generate-report", {
            method: "POST",
            body: JSON.stringify({
                report_type: reportType,
                parameters: parameters,
                export_format: exportFormat
            })
        });
    } catch (err) {
        console.error("Generate report error:", err);
        throw err;
    }
}

async function getReports(skip = 0, limit = 10) {
    try {
        return await apiFetch(`/analytics/reports?skip=${skip}&limit=${limit}`);
    } catch (err) {
        console.error("Get reports error:", err);
        throw err;
    }
}

async function exportReport(reportId) {
    try {
        return await apiFetch(`/analytics/reports/${reportId}/export`);
    } catch (err) {
        console.error("Export report error:", err);
        throw err;
    }
}
