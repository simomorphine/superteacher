document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('td').forEach(td => {
        td.addEventListener('click', () => {
            let svgDoesNotExist = true;

            // If the <td> already contains an input, don't do anything
            if (td.querySelector('input')) {
                return;
            }

            // Store the current text content
            const currentText = td.innerText.trim();

            // Create an input element
            const input = document.createElement('input');
            input.type = 'text';
            input.value = currentText;
            input.style.width = '100%'; // Make the input full width to fit the <td>

            // Clear the <td> content and append the input
            td.innerHTML = '';
            td.appendChild(input);

            // Focus on the input
            input.focus();

            // When the input loses focus, replace it with the input's value
            input.addEventListener('blur', () => {
                td.innerText = input.value.trim() || currentText; // Set to original if input is empty
                if (svgDoesNotExist && td.textContent) {
                    addSvgButtonIcons(td, svgMarkup, removeSvgMarkup, 'bottom-right', handleColspanClick, handleRemoveClick);
                    svgDoesNotExist = false;
                }
            });

            // Handle "Enter" key to finalize input
            input.addEventListener('keydown', (event) => {
                if (event.key === 'Enter') {
                    input.blur(); // Trigger blur event to finalize input
                    if (svgDoesNotExist && td.textContent) {
                        addSvgButtonIcons(td, svgMarkup, removeSvgMarkup, 'bottom-right', handleColspanClick, handleRemoveClick);
                        svgDoesNotExist = false;
                    }
                }
            });
        });
    });
});

function addSvgButtonIcons(tableData, svgMarkup, removeSvgMarkup, position, onClick, removeClick) {
    // Remove any existing SVG buttons
    const existingButtons = tableData.querySelectorAll('.positioned-svg');
    existingButtons.forEach(button => button.remove());

    tableData.classList.add('relative-td');

    // Create the expand button
    const expandButton = document.createElement('button');
    expandButton.classList.add('positioned-svg', 'expand');
    expandButton.style.height = '100%'; // Ensure it scales with cell height
    expandButton.innerHTML = svgMarkup; // Expand SVG markup

    expandButton.addEventListener('click', () => {
        onClick(tableData);
        tableData.classList.add('colspan-animation');
        setTimeout(() => tableData.classList.remove('colspan-animation'), 500); // Animation duration
    });

    // Create the remove button
    const removeButton = document.createElement('button');
    removeButton.classList.add('positioned-svg', 'remove');
    removeButton.innerHTML = removeSvgMarkup; // Remove SVG markup

    removeButton.addEventListener('click', () => {
        tableData.innerHTML = ''; // Clear the cell
        addSvgButtonIcons(tableData, svgMarkup, removeSvgMarkup, 'bottom-right', handleColspanClick, handleRemoveClick); // Re-add SVG buttons if necessary
    });

    tableData.appendChild(expandButton);
    tableData.appendChild(removeButton);
}

// Define your SVG markup for expand button
const svgMarkup = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 24" width="30" height="30" fill="#54f5a5">
    <line x1="4" y1="2" x2="4" y2="22" stroke="#54f5a5" stroke-width="2"/>
    <path d="M10 4l8 8-8 8z"/>
</svg>`;

// Define your SVG markup for remove button
const removeSvgMarkup = `
<svg 
    xmlns="http://www.w3.org/2000/svg" 
    width="24" 
    height="24" 
    viewBox="0 0 24 24" 
    fill="none" 
    stroke="currentColor" 
    stroke-width="2" 
    stroke-linecap="round" 
    stroke-linejoin="round"
>
    <path d="M18 6L6 18" />
    <path d="M6 6l12 12" />
</svg>`;

// Handle click event for the expand button to adjust colspan
function handleColspanClick(tdElement) {
    const maxColspan = 4; // Set the maximum colspan limit
    let currentColspan = parseInt(tdElement.getAttribute('colspan') || '1', 10);

    if (currentColspan < maxColspan) {
        currentColspan++;
    } else {
        currentColspan = 1; // Reset to 1 if maximum reached
    }
    tdElement.setAttribute('colspan', currentColspan);
}

// Handle click event for the remove button
function handleRemoveClick(tdElement) {
    tdElement.innerHTML = ''; // Clear cell content
    // Re-add SVG buttons if necessary
    addSvgButtonIcons(tdElement, svgMarkup, removeSvgMarkup, 'bottom-right', handleColspanClick, handleRemoveClick);
}