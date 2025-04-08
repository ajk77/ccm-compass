  
  /***
  For CompassDataTables.html
  ***/
  function toggleSubTable(id) {
    const subTable = document.getElementById(id);
    
    // Ensure the initial display property is set to 'none' if undefined
    if (!subTable.style.display) {
      subTable.style.display = 'none';
    }
    
    // Toggle display between 'none' and 'table-row'
    subTable.style.display = (subTable.style.display === 'none') ? 'table-row' : 'none';
  }
  
  /***
  For ConceptSelectionForm.html
  ***/
 function toggle(id, iconId) {
	let element = document.getElementById(id);
	let icon = document.getElementById(iconId);
	if (element.style.display === '' || element.style.display === 'none') {
		element.style.display = 'block';
		icon.textContent = '▼';
	} else {
		element.style.display = 'none';
		icon.textContent = '▶';
	}
};

function toggleGroup(groupCheckbox, groupId) {
	let checkboxes = document.querySelectorAll('.' + groupId);
	checkboxes.forEach(checkbox => {
		checkbox.checked = groupCheckbox.checked;
	});
};

function downloadList() {
// Get all checked checkboxes
const checkedItems = Array.from(document.querySelectorAll('input[name="concept"]:checked'))
	.map(item => item.value);

if (checkedItems.length === 0) {
	alert('Please select at least one item!');
	return;
}

// Create the content for the file
const content = "Selected Items:" + checkedItems.join(';');

// Create a blob with the content
const blob = new Blob([content], { type: 'text/plain' });

// Create a temporary URL for the blob
const url = window.URL.createObjectURL(blob);

// Create a temporary link element
const link = document.createElement('a');
link.href = url;
link.download = 'selected_items.txt';

// Programmatically click the link to trigger download
document.body.appendChild(link);
link.click();

// Clean up
document.body.removeChild(link);
window.URL.revokeObjectURL(url);
};