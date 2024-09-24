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
// document.addEventListener('DOMContentLoaded', () =>{
//     document.querySelectorAll('td').forEach(td => {
//         td.addEventListener('click', () =>{
//             if (td.textContent){
//                 const expandIcon = document.createElement('img');
//                 expandIcon.classList.add('bottom-right');
//                 expandIcon.src = '../static/assets/arrow.png';
//                 expandIcon.style.height = td.offsetHeight;
//                 td.appendChild(expandIcon);
//             }
//         });
//     });
// });
// handle the calender here
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('td').forEach(td => {
        td.addEventListener('click', () => {

            // If the <td> already contains an input, don't do anything
            if (td.querySelector('input')) return;

            // Store the current text content
            const currentText = td.innerText.trim();

            // Create an input element
            const input = document.createElement('input');
            input.type = 'text';
            input.value = currentText;
            input.style.width = '100%'; // Optional: Make the input full width to fit the <td>

            // Clear the <td> content and append the input
            td.innerHTML = '';
            td.appendChild(input);

            // Focus on the input
            input.focus();

            // When the input loses focus, replace it with the input's value
            input.addEventListener('blur', () => {
                td.innerText = input.value.trim() || currentText; // Set to original if input is empty
                //add icons if not exist
                if (imagedoesNotExist){}
                        addImageButton(expandIcon);
                        addImageButton(deleteIcon);
                        changeColor(td);
                // const expandIcon = document.createElement('img');
                // expandIcon.classList.add('bottom-right');
                // expandIcon.src = '../static/assets/arrow.png';
                // expandIcon.style.height = td.offsetHeight;
                // td.appendChild(expandIcon);
            });

            // Handle "Enter" key to finalize input
            input.addEventListener('keydown', (event) => {
                if (event.key === 'Enter') {
                    input.blur(); // Trigger blur event to finalize input
                    //add icons if not exist
                    addImageButton(expandIcon);
                    addImageButton(deleteIcon);
                    changeColor(td);
                    // const expandIcon = document.createElement('img');
                    // expandIcon.classList.add('bottom-right');
                    // expandIcon.src = '../static/assets/arrow.png';
                    // expandIcon.style.height = td.offsetHeight;
                    // td.appendChild(expandIcon);
                }
            });
        });
    });
    
});


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

document.getElementById('submit-btn').addEventListener('click', () => {
    if (!validateSection()) return;

    console.log('User Preferences:', userPreferences);
    submitPreferences();
});

// Functions
// need to modify this function
function collectScheduleData() {
    console.log("im inside");
    const table = document.getElementById('schedule-table');
    const rows = table.querySelectorAll('tbody tr');
    const timeSlots = Array.from(table.querySelectorAll('thead th')).slice(1);

    rows.forEach(row => {
        const day = row.querySelector('th').textContent.trim();
        const cells = row.querySelectorAll('td');

        // Initialize the day array if it doesn't exist
        if (!userPreferences.schedule[day]) {
            userPreferences.schedule[day] = [];
        }

        cells.forEach((cell, index) => {
            const description = cell.textContent.trim();
            if (description) {
                const time = timeSlots[index].textContent.trim();
                userPreferences.schedule[day].push({ time, description });
            }
        });
    });
}


//collect holiday data here
// function collectHolidaysData() {
// }

function navigateSections(direction) {
    // Hide current section
    document.getElementById(sections[currentSectionIndex]).style.display = 'none';

    // Move to the next/previous section
    currentSectionIndex += direction;
    currentSectionIndex = Math.max(0, Math.min(currentSectionIndex, sections.length - 1));
    //skep the language section if the subject is a language
    // Show new section
    document.getElementById(sections[currentSectionIndex]).style.display = 'block';

    // Toggle button visibility
    document.getElementById('previous-btn').style.display = currentSectionIndex > 0 ? 'inline-block' : 'none';
    document.getElementById('next-btn').style.display = currentSectionIndex < sections.length - 1 ? 'inline-block' : 'none';
    document.getElementById('submit-btn').style.display = currentSectionIndex === sections.length - 1 ? 'inline-block' : 'none';
    if (sections[currentSectionIndex] === 'schedule-section' || sections[currentSectionIndex] === 'holidays-section') {
        document.getElementById('skep').style.display = 'inline-block';
    }else{
        document.getElementById('skep').style.display = 'none';
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
        isValid = false;}
    // } else if (currentSectionId === 'schedule-section' && Object.keys(userPreferences.schedule).length === 0) {
    //     displayError('schedule-error', true);
    //     isValid = false;
    // } else if (currentSectionId === 'holidays-section' && userPreferences.holidays.length === 0) {
    //     displayError('holidays-error', true);
    //     isValid = false;
    // }

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
