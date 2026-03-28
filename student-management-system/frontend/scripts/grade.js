class GradeManager {
    constructor() {
        this.form = document.getElementById('grade-form');
        this.list = document.getElementById('grade-list');
        this.form.addEventListener('submit', this.addGrade.bind(this));
        this.loadGrades();
    }

    async addGrade(e) {
        e.preventDefault();
        const data = { student_id: +document.getElementById('student_id').value, course_id: +document.getElementById('course_id').value, grade: +document.getElementById('grade').value };
        await fetch('http://localhost:8000/grades/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
        this.loadGrades();
    }

    async loadGrades() {
        const response = await fetch('http://localhost:8000/grades/');
        const grades = await response.json();
        this.list.innerHTML = grades.map(g => `<li>Student ${g.student_id} - Course ${g.course_id} - ${g.grade}</li>`).join('');
    }
}

const gradeManager = new GradeManager();
