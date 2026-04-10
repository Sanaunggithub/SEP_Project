class GradeManager {
    constructor() {
        this.form = document.getElementById('grade-form');
        this.list = document.getElementById('grade-list');
        if (this.form) this.form.addEventListener('submit', this.addGrade.bind(this)); // only once
        if (this.list) this.loadGrades();
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

async function getGrades(studentId = "", courseId = "", skip = 0, limit = 10) {
    try {
        let url = `/grades/?skip=${skip}&limit=${limit}`;
        if (studentId) url += `&student_id=${studentId}`;
        if (courseId) url += `&course_id=${courseId}`;
        return await apiFetch(url);
    } catch (err) {
        console.error("Get grades error:", err);
        throw err;
    }
}

async function createGrade(studentId, courseId, componentType, score, maxScore, weight, remarks) {
    try {
        return await apiFetch("/grades/", {
            method: "POST",
            body: JSON.stringify({
                student_id: studentId,
                course_id: courseId,
                component_type: componentType,
                score: score,
                max_score: maxScore,
                weight: weight,
                remarks: remarks
            })
        });
    } catch (err) {
        console.error("Create grade error:", err);
        throw err;
    }
}

async function updateGrade(gradeId, studentId, courseId, componentType, score, maxScore, weight, remarks) {
    try {
        return await apiFetch(`/grades/${gradeId}`, {
            method: "PUT",
            body: JSON.stringify({
                student_id: studentId,
                course_id: courseId,
                component_type: componentType,
                score: score,
                max_score: maxScore,
                weight: weight,
                remarks: remarks
            })
        });
    } catch (err) {
        console.error("Update grade error:", err);
        throw err;
    }
}

async function deleteGrade(gradeId) {
    try {
        return await apiFetch(`/grades/${gradeId}`, { method: "DELETE" });
    } catch (err) {
        console.error("Delete grade error:", err);
        throw err;
    }
}

async function getStudentGPA(studentId) {
    try {
        return await apiFetch(`/grades/gpa/${studentId}`);
    } catch (err) {
        console.error("Get student GPA error:", err);
        throw err;
    }
}

async function getGradeReport(courseId) {
    try {
        return await apiFetch(`/grades/report/${courseId}`);
    } catch (err) {
        console.error("Get grade report error:", err);
        throw err;
    }
}
