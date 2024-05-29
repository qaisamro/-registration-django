document.getElementById('course-form').addEventListener('submit', function(e) {
    e.preventDefault();
    var courseName = document.getElementById('course-name').value;
    if (courseName.trim() !== '') {
        addCourse(courseName);
        document.getElementById('course-name').value = '';
    }
});

function addCourse(courseName) {
    var courseList = document.getElementById('course-list');
    var li = document.createElement('li');
    li.textContent = courseName;
    courseList.appendChild(li);
}


// script.js

document.getElementById("course-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form submission

    var courseName = document.getElementById("course-name").value;

    // Create a new list item for the course
    var listItem = document.createElement("li");
    listItem.textContent = courseName;

    // Add the new list item to the course list
    document.getElementById("course-list").appendChild(listItem);

    // Clear the input field
    document.getElementById("course-name").value = "";
});
