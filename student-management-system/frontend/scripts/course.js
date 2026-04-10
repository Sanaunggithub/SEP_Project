class CourseManager {
    constructor() {
        this.form = document.getElementById('course-form');
        this.list = document.getElementById('course-list');
        this.form.addEventListener('submit', this.addCourse.bind(this));
        if(this.form) this.loadCourses();
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

async function getCourses(semester = "", skip = 0, limit = 10) {
    try {
        let url = `/courses/?skip=${skip}&limit=${limit}`;
        if (semester) url += `&semester=${semester}`;
        return await apiFetch(url);
    } catch (err) {
        console.error("Get courses error:", err);
        throw err;
    }
}

async function getCourse(courseId) {
    try {
        return await apiFetch(`/courses/${courseId}`);
    } catch (err) {
        console.error("Get course error:", err);
        throw err;
    }
}

async function createCourse(courseCode, title, description, creditHours, maxSeats, scheduleDays, startTime, endTime, semester, year, roomLocation, instructorId) {
    try {
        return await apiFetch("/courses/", {
            method: "POST",
            body: JSON.stringify({
                course_code: courseCode,
                title: title,
                description: description,
                credit_hours: creditHours,
                max_seats: maxSeats,
                schedule_days: scheduleDays,
                start_time: startTime,
                end_time: endTime,
                semester: semester,
                year: year,
                room_location: roomLocation,
                instructor_id: instructorId
            })
        });
    } catch (err) {
        console.error("Create course error:", err);
        throw err;
    }
}

async function updateCourse(courseId, title, description, creditHours, maxSeats, scheduleDays, startTime, endTime, roomLocation, status) {
    try {
        const updates = {};
        if (title !== undefined) updates.title = title;
        if (description !== undefined) updates.description = description;
        if (creditHours !== undefined) updates.credit_hours = creditHours;
        if (maxSeats !== undefined) updates.max_seats = maxSeats;
        if (scheduleDays !== undefined) updates.schedule_days = scheduleDays;
        if (startTime !== undefined) updates.start_time = startTime;
        if (endTime !== undefined) updates.end_time = endTime;
        if (roomLocation !== undefined) updates.room_location = roomLocation;
        if (status !== undefined) updates.status = status;

        return await apiFetch(`/courses/${courseId}`, {
            method: "PUT",
            body: JSON.stringify(updates)
        });
    } catch (err) {
        console.error("Update course error:", err);
        throw err;
    }
}

async function deleteCourse(courseId) {
    try {
        return await apiFetch(`/courses/${courseId}`, { method: "DELETE" });
    } catch (err) {
        console.error("Delete course error:", err);
        throw err;
    }
}

async function enrollStudent(courseId, studentId) {
    try {
        return await apiFetch(`/courses/${courseId}/enroll?student_id=${studentId}`, { method: "POST" });
    } catch (err) {
        console.error("Enroll student error:", err);
        throw err;
    }
}

async function unenrollStudent(courseId, studentId) {
    try {
        return await apiFetch(`/courses/${courseId}/enroll?student_id=${studentId}`, { method: "DELETE" });
    } catch (err) {
        console.error("Unenroll student error:", err);
        throw err;
    }
}

async function getCourseStudents(courseId) {
    try {
        return await apiFetch(`/courses/${courseId}/students`);
    } catch (err) {
        console.error("Get course students error:", err);
        throw err;
    }
}

async function getCourseSchedule(courseId) {
    try {
        return await apiFetch(`/courses/${courseId}/schedule`);
    } catch (err) {
        console.error("Get course schedule error:", err);
        throw err;
    }
}


