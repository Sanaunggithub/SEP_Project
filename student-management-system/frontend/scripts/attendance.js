class AttendanceManager {
    constructor() {
        this.form = document.getElementById('attendance-form');
        this.list = document.getElementById('attendance-list');
        if (this.form) this.form.addEventListener('submit', this.addAttendance.bind(this));
        if (this.list) this.loadAttendance();
    }

    async addAttendance(e) {
        e.preventDefault();
        const data = { student_id: +document.getElementById('student_id').value, course_id: +document.getElementById('course_id').value, date: document.getElementById('date').value, present: document.getElementById('present').checked };
        await fetch('http://localhost:8000/attendance/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
        this.loadAttendance();
    }

    async loadAttendance() {
        const response = await fetch('http://localhost:8000/attendance/');
        const attendance = await response.json();
        this.list.innerHTML = attendance.map(a => `<li>Student ${a.student_id} - Course ${a.course_id} - ${a.date} - ${a.present ? 'Present' : 'Absent'}</li>`).join('');
    }
}

const attendanceManager = new AttendanceManager();

async function createAttendance(studentId, courseId, date, status, checkInTime) {
    try {
        const payload = {
            student_id: studentId,
            course_id: courseId,
            date: date,
            status: status
        };
        if (checkInTime) payload.check_in_time = checkInTime;

        return await apiFetch("/attendance/", {
            method: "POST",
            body: JSON.stringify(payload)
        });
    } catch (err) {
        console.error("Create attendance error:", err);
        throw err;
    }
}

async function getCourseAttendance(courseId, dateFrom = "", dateTo = "", skip = 0, limit = 10) {
    try {
        let url = `/attendance/${courseId}?skip=${skip}&limit=${limit}`;
        if (dateFrom) url += `&date_from=${dateFrom}`;
        if (dateTo) url += `&date_to=${dateTo}`;
        return await apiFetch(url);
    } catch (err) {
        console.error("Get course attendance error:", err);
        throw err;
    }
}

async function getStudentAttendanceRecords(studentId, courseId = "", skip = 0, limit = 10) {
    try {
        let url = `/attendance/student/${studentId}?skip=${skip}&limit=${limit}`;
        if (courseId) url += `&course_id=${courseId}`;
        return await apiFetch(url);
    } catch (err) {
        console.error("Get student attendance error:", err);
        throw err;
    }
}

async function updateAttendanceStatus(attendanceId, statusUpdate) {
    try {
        return await apiFetch(`/attendance/${attendanceId}?status_update=${statusUpdate}`, {
            method: "PUT"
        });
    } catch (err) {
        console.error("Update attendance status error:", err);
        throw err;
    }
}

async function bulkCreateAttendance(courseId, date, records) {
    try {
        return await apiFetch("/attendance/bulk", {
            method: "POST",
            body: JSON.stringify({
                course_id: courseId,
                date: date,
                records: records
            })
        });
    } catch (err) {
        console.error("Bulk create attendance error:", err);
        throw err;
    }
}

async function getAtRiskStudents(threshold = 75.0) {
    try {
        return await apiFetch(`/attendance/at-risk?threshold=${threshold}`);
    } catch (err) {
        console.error("Get at-risk students error:", err);
        throw err;
    }
}
