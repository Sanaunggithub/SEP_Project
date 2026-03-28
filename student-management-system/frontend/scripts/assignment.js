class AssignmentManager {
    constructor() {
        this.form = document.getElementById('assignment-form');
        this.list = document.getElementById('assignment-list');
        this.form.addEventListener('submit', this.addAssignment.bind(this));
        this.loadAssignments();
    }

    async addAssignment(e) {
        e.preventDefault();
        const data = { course_id: +document.getElementById('course_id').value, title: document.getElementById('title').value, due_date: document.getElementById('due_date').value };
        await fetch('http://localhost:8000/assignments/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
        this.loadAssignments();
    }

    async loadAssignments() {
        const response = await fetch('http://localhost:8000/assignments/');
        const assignments = await response.json();
        this.list.innerHTML = assignments.map(a => `<li>Course ${a.course_id} - ${a.title} - Due ${a.due_date}</li>`).join('');
    }
}

const assignmentManager = new AssignmentManager();
