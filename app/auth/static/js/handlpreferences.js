// Store user preferences
const userPreferences = {
    teacherType: null,
    subject: null,
    schoolName: '',
    language: null,
    schedule: {},
    holidays: []
};

let currentSectionIndex = 0;
const sections = [
    'teacher-type-section',
    'subject-section',
    'language-section',
    'school-name-section',
    'schedule-section',
    'holidays-section'
];

// Initialize
document.getElementById(sections[currentSectionIndex]).style.display = 'block';

// Event listeners for choice buttons
document.querySelectorAll('.btn-choice').forEach(button => {
    button.addEventListener('click', (event) => {
        const sectionId = event.target.closest('.choice-section').id;
        const choice = event.target.getAttribute('data-choice');

        if (sectionId === 'teacher-type-section') {
            userPreferences.teacherType = choice;
        } else if (sectionId === 'subject-section') {
            userPreferences.subject = choice;
        } else if (sectionId === 'language-section') {
            userPreferences.language = choice;
        }

        // Hide error message if a choice is made
        document.getElementById(`${sectionId}-error`).style.display = 'none';
    });
});

// Navigation button event listeners
// need to modify this
document.getElementById('next-btn').addEventListener('click', () => {
    if (!validateSection()) return;

    // Save data based on the current section
    if (sections[currentSectionIndex] === 'school-name-section') {
        userPreferences.schoolName = document.getElementById('school-name').value;
    } else if (sections[currentSectionIndex] === 'schedule-section') {
        collectScheduleData();
    } else if (sections[currentSectionIndex] === 'holidays-section') {
        collectHolidaysData();
    }

    navigateSections(1);
});
document.getElementById('skep').addEventListener('click', () =>{
    Array.from(document.getElementsByClassName('error-message')).forEach(errorMessage => {
        errorMessage.style.display = 'none';
    });
    navigateSections(1);
});
document.getElementById('previous-btn').addEventListener('click', () => {
    Array.from(document.getElementsByClassName('error-message')).forEach(errorMessage => {
        errorMessage.style.display = 'none';
    });
    navigateSections(-1);
});

// need to work in here
document.getElementById('skip-schedule-btn').addEventListener('click', () => {
    document.getElementById('next-btn').click();
});

document.getElementById('submit-btn').addEventListener('click', () => {
    if (!validateSection()) return;

    console.log('User Preferences:', userPreferences);
    submitPreferences();
});

// Functions
// need to modify this function
function collectScheduleData() {
    // Collect schedule data manually without Flikker
    document.querySelectorAll('#schedule-table td.selected').forEach(cell => {
        const day = cell.dataset.day; // Assuming each cell has a `data-day` attribute
        userPreferences.schedule[day] = cell.textContent;
    });
}
// need to modify this function
function collectHolidaysData() {
    userPreferences.holidays = [];
    document.querySelectorAll('#holidays-list input').forEach(input => {
        if (input.value) {
            userPreferences.holidays.push(input.value);
        }
    });
}

function navigateSections(direction) {
    // Hide current section
    document.getElementById(sections[currentSectionIndex]).style.display = 'none';

    // Move to the next/previous section
    currentSectionIndex += direction;
    currentSectionIndex = Math.max(0, Math.min(currentSectionIndex, sections.length - 1));

    // Show new section
    document.getElementById(sections[currentSectionIndex]).style.display = 'block';

    // Toggle button visibility
    document.getElementById('previous-btn').style.display = currentSectionIndex > 0 ? 'inline-block' : 'none';
    document.getElementById('next-btn').style.display = currentSectionIndex < sections.length - 1 ? 'inline-block' : 'none';
    document.getElementById('submit-btn').style.display = currentSectionIndex === sections.length - 1 ? 'inline-block' : 'none';
    if (sections[currentSectionIndex] === 'schedule-section' || sections[currentSectionIndex] === 'holidays-section') {
        document.getElementById('skep').style.display = 'inline-block';
    }
}

function validateSection() {
    const currentSectionId = sections[currentSectionIndex];
    let isValid = true;

    if (currentSectionId === 'teacher-type-section' && !userPreferences.teacherType) {
        displayError('teacher-type-error', true);
        isValid = false;
    } else if (currentSectionId === 'subject-section' && !userPreferences.subject) {
        displayError('subject-error', true);
        isValid = false;
    } else if (currentSectionId === 'school-name-section' && !document.getElementById('school-name').value) {
        displayError('school-name-error', true);
        isValid = false;
    } else if (currentSectionId === 'language-section' && !userPreferences.language) {
        displayError('language-error', true);
        isValid = false;
    } else if (currentSectionId === 'schedule-section' && Object.keys(userPreferences.schedule).length === 0) {
        displayError('schedule-error', true);
        isValid = false;
    }

    return isValid;
}

function displayError(errorId, show) {
    document.getElementById(errorId).style.display = show ? 'block' : 'none';
}

function submitPreferences() {
    fetch('/save_preferences', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userPreferences),
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        alert('Preferences saved successfully!');
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// let work with calender
document.getElementsByTagName('td').addEventListener('click')

