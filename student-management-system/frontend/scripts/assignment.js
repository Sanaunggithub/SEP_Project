class AssignmentManager {
    constructor() {
        this.form = document.getElementById('assignment-form');
        this.list = document.getElementById('assignment-list');
        if (this.form) this.form.addEventListener('submit', this.addAssignment.bind(this));
        if (this.list) this.loadAssignments();
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

async function getAssignments(courseId = "", skip = 0, limit = 10) {
    try {
        let url = `/assignments/?skip=${skip}&limit=${limit}`;
        if (courseId) url += `&course_id=${courseId}`;
        return await apiFetch(url);
    } catch (err) {
        console.error("Get assignments error:", err);
        throw err;
    }
}

async function getAssignment(assignmentId) {
    try {
        return await apiFetch(`/assignments/${assignmentId}`);
    } catch (err) {
        console.error("Get assignment error:", err);
        throw err;
    }
}

async function createAssignment(courseId, title, description, dueDate, maxScore, allowLateSubmission, latePenaltyPercent, fileTypesAllowed) {
    try {
        return await apiFetch("/assignments/", {
            method: "POST",
            body: JSON.stringify({
                course_id: courseId,
                title: title,
                description: description,
                due_date: dueDate,
                max_score: maxScore,
                allow_late_submission: allowLateSubmission,
                late_penalty_percent: latePenaltyPercent,
                file_types_allowed: fileTypesAllowed
            })
        });
    } catch (err) {
        console.error("Create assignment error:", err);
        throw err;
    }
}

async function updateAssignment(assignmentId, title, description, dueDate, maxScore, allowLateSubmission, latePenaltyPercent) {
    try {
        const updates = {};
        if (title !== undefined) updates.title = title;
        if (description !== undefined) updates.description = description;
        if (dueDate !== undefined) updates.due_date = dueDate;
        if (maxScore !== undefined) updates.max_score = maxScore;
        if (allowLateSubmission !== undefined) updates.allow_late_submission = allowLateSubmission;
        if (latePenaltyPercent !== undefined) updates.late_penalty_percent = latePenaltyPercent;

        return await apiFetch(`/assignments/${assignmentId}`, {
            method: "PUT",
            body: JSON.stringify(updates)
        });
    } catch (err) {
        console.error("Update assignment error:", err);
        throw err;
    }
}

async function deleteAssignment(assignmentId) {
    try {
        return await apiFetch(`/assignments/${assignmentId}`, { method: "DELETE" });
    } catch (err) {
        console.error("Delete assignment error:", err);
        throw err;
    }
}

async function submitAssignment(assignmentId, file) {
    try {
        const formData = new FormData();
        formData.append("file", file);

        return await apiFetch(`/assignments/${assignmentId}/submit`, {
            method: "POST",
            body: formData
        });
    } catch (err) {
        console.error("Submit assignment error:", err);
        throw err;
    }
}

async function getSubmissions(assignmentId, skip = 0, limit = 10) {
    try {
        return await apiFetch(`/assignments/${assignmentId}/submissions?skip=${skip}&limit=${limit}`);
    } catch (err) {
        console.error("Get submissions error:", err);
        throw err;
    }
}

async function getSubmission(submissionId) {
    try {
        return await apiFetch(`/assignments/submissions/${submissionId}`);
    } catch (err) {
        console.error("Get submission error:", err);
        throw err;
    }
}

async function gradeSubmission(submissionId, score, feedback, status, plagiarismScore) {
    try {
        const payload = {
            score: score,
            feedback: feedback,
            status: status
        };
        if (plagiarismScore !== undefined) payload.plagiarism_score = plagiarismScore;

        return await apiFetch(`/assignments/submissions/${submissionId}/grade`, {
            method: "PUT",
            body: JSON.stringify(payload)
        });
    } catch (err) {
        console.error("Grade submission error:", err);
        throw err;
    }
}