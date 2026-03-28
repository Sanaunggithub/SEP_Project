class CourseManager {
    constructor() {
        this.form = document.getElementById('course-form');
        this.list = document.getElementById('course-list');
        this.form.addEventListener('submit', this.addCourse.bind(this));
        this.loadCourses();
    }

    async addCourse(e) {
        e.preventDefault();
        const data = { name: document.getElementById('name').value, description: document.getElementById('description').value };
        await fetch('http://localhost:8000/courses/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
        this.loadCourses();
    }

    async loadCourses() {
        const response = await fetch('http://localhost:8000/courses/');
        const courses = await response.json();
        this.list.innerHTML = courses.map(c => `<li>${c.name} - ${c.description}</li>`).join('');
    }
}

const courseManager = new CourseManager();
