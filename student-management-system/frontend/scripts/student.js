// ─── Legacy class (kept but isolated) ────────────────────────────────────────
class StudentManager {
    constructor() {
        // Only initialize if these elements actually exist on the page
        this.form = document.getElementById('student-form');
        this.list = document.getElementById('student-list');
        if (this.form) this.form.addEventListener('submit', this.addStudent.bind(this));
        if (this.list) this.loadStudents();
    }

    async addStudent(e) {
        e.preventDefault();
        const data = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value
        };
        await fetch('http://localhost:8000/students/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        this.loadStudents();
    }

    async loadStudents() {
        const response = await fetch('http://localhost:8000/students/');
        const students = await response.json();
        this.list.innerHTML = students.map(s => `<li>${s.name} - ${s.email}</li>`).join('');
    }
}

const studentManager = new StudentManager();

// ─── Global functions (OUTSIDE the class) ────────────────────────────────────

async function getStudents(skip = 0, limit = 10) {
    try {
        return await apiFetch(`/students/?skip=${skip}&limit=${limit}`);
    } catch (err) {
        console.error("Get students error:", err);
        throw err;
    }
}

async function getStudent(studentId) {
    try {
        return await apiFetch(`/students/${studentId}`);
    } catch (err) {
        console.error("Get student error:", err);
        throw err;
    }
}

async function createStudent(userId, studentIdNumber, enrollmentDate, program, department, yearLevel, scholarshipStatus, guardianName, guardianPhone, guardianEmail) {
    try {
        return await apiFetch("/students/", {
            method: "POST",
            body: JSON.stringify({
                user_id: userId,
                student_id_number: studentIdNumber,
                enrollment_date: enrollmentDate,
                program: program,
                department: department,
                year_level: yearLevel,
                scholarship_status: scholarshipStatus,
                guardian_name: guardianName,
                guardian_phone: guardianPhone,
                guardian_email: guardianEmail
            })
        });
    } catch (err) {
        console.error("Create student error:", err);
        throw err;
    }
}

async function updateStudent(studentId, program, department, yearLevel, scholarshipStatus, academicStatus, gpa, guardianName, guardianPhone, guardianEmail, notes) {
    try {
        const updates = {};
        if (program !== undefined) updates.program = program;
        if (department !== undefined) updates.department = department;
        if (yearLevel !== undefined) updates.year_level = yearLevel;
        if (scholarshipStatus !== undefined) updates.scholarship_status = scholarshipStatus;
        if (academicStatus !== undefined) updates.academic_status = academicStatus;
        if (gpa !== undefined) updates.gpa = gpa;
        if (guardianName !== undefined) updates.guardian_name = guardianName;
        if (guardianPhone !== undefined) updates.guardian_phone = guardianPhone;
        if (guardianEmail !== undefined) updates.guardian_email = guardianEmail;
        if (notes !== undefined) updates.notes = notes;

        return await apiFetch(`/students/${studentId}`, {
            method: "PUT",
            body: JSON.stringify(updates)
        });
    } catch (err) {
        console.error("Update student error:", err);
        throw err;
    }
}

async function deleteStudent(studentId) {
    try {
        return await apiFetch(`/students/${studentId}`, { method: "DELETE" });
    } catch (err) {
        console.error("Delete student error:", err);
        throw err;
    }
}

async function getStudentCourses(studentId) {
    try {
        return await apiFetch(`/students/${studentId}/courses`);
    } catch (err) {
        console.error("Get student courses error:", err);
        throw err;
    }
}

async function getStudentGrades(studentId) {
    try {
        return await apiFetch(`/students/${studentId}/grades`);
    } catch (err) {
        console.error("Get student grades error:", err);
        throw err;
    }
}

async function getStudentAttendance(studentId) {
    try {
        return await apiFetch(`/students/${studentId}/attendance`);
    } catch (err) {
        console.error("Get student attendance error:", err);
        throw err;
    }
}

async function getStudentByUserId(userId) {
    try {
        return await apiFetch(`/students/by-user/${userId}`);
    } catch (err) {
        console.error("Get student by user error:", err);
        throw err;
    }
}