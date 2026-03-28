class AttendanceManager {
    constructor() {
        this.form = document.getElementById('attendance-form');
        this.list = document.getElementById('attendance-list');
        this.form.addEventListener('submit', this.addAttendance.bind(this));
        this.loadAttendance();
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
