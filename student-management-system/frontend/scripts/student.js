class StudentManager {
    constructor() {
        this.form = document.getElementById('student-form');
        this.list = document.getElementById('student-list');
        this.form.addEventListener('submit', this.addStudent.bind(this));
        this.loadStudents();
    }

    async addStudent(e) {
        e.preventDefault();
        const data = { name: document.getElementById('name').value, email: document.getElementById('email').value };
        await fetch('http://localhost:8000/students/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
        this.loadStudents();
    }

    async loadStudents() {
        const response = await fetch('http://localhost:8000/students/');
        const students = await response.json();
        this.list.innerHTML = students.map(s => `<li>${s.name} - ${s.email}</li>`).join('');
    }
}

const studentManager = new StudentManager();
