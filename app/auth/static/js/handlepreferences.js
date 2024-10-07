document.addEventListener("DOMContentLoaded", function () {
    let currentSectionIndex = 0;
    const sections = document.querySelectorAll(".choice-section");
    const nextBtn = document.getElementById("next-btn");
    const previousBtn = document.getElementById("previous-btn");
    const submitBtn = document.getElementById("submit-btn");

    const preferences = {
        teacherType: null,
        subject: null,
        language: null,
        schoolName: null
    };

    function showSection(index) {
        sections.forEach((section, i) => {
            section.style.display = i === index ? "block" : "none";
        });
        previousBtn.style.display = index > 0 ? "inline-block" : "none";
        nextBtn.style.display = index < sections.length - 1 ? "inline-block" : "none";
        submitBtn.style.display = index === sections.length - 1 ? "inline-block" : "none";
    }

    function validateCurrentSection() {
        const currentSection = sections[currentSectionIndex];
        const errorMessages = currentSection.querySelectorAll(".error-message");

        errorMessages.forEach((error) => (error.style.display = "none"));

        if (currentSection.id === "teacher-type-section" && !preferences.teacherType) {
            document.getElementById("teacher-type-error").style.display = "block";
            return false;
        }

        if (currentSection.id === "subject-section" && !preferences.subject) {
            document.getElementById("subject-error").style.display = "block";
            return false;
        }

        if (currentSection.id === "language-section" && !preferences.language) {
            document.getElementById("language-error").style.display = "block";
            return false;
        }

        if (currentSection.id === "school-name-section") {
            const schoolNameInput = document.getElementById("school-name");
            if (schoolNameInput.value.trim() === "") {
                document.getElementById("school-name-error").style.display = "block";
                return false;
            }
            preferences.schoolName = schoolNameInput.value.trim();
        }

        return true;
    }

    document.querySelectorAll(".btn-choice").forEach((button) => {
        button.addEventListener("click", function () {
            const choice = this.getAttribute("data-choice");
            const sectionId = this.closest(".choice-section").id;

            if (sectionId === "teacher-type-section") {
                preferences.teacherType = choice;
            } else if (sectionId === "subject-section") {
                preferences.subject = choice;
            } else if (sectionId === "language-section") {
                preferences.language = choice;
            }
        });
    });

    nextBtn.addEventListener("click", function () {
        if (validateCurrentSection()) {
            currentSectionIndex++;
            showSection(currentSectionIndex);
        }
    });

    previousBtn.addEventListener("click", function () {
        currentSectionIndex--;
        showSection(currentSectionIndex);
    });

    submitBtn.addEventListener("click", function () {
        if (validateCurrentSection()) {
            // Submit the preferences to the server
            fetch("/submit-preferences", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(preferences)
            })
                .then((response) => {
                    if (response.ok) {
                        alert("Preferences submitted successfully!");
                    } else {
                        alert("Failed to submit preferences.");
                    }
                })
                .catch((error) => {
                    console.error("Error submitting preferences:", error);
                    alert("Error submitting preferences.");
                });
        }
    });

    showSection(currentSectionIndex);
});
