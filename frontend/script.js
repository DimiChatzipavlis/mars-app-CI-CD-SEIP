const resourceList = document.getElementById('resource-list');
const addResourceForm = document.getElementById('add-resource-form');
const updateResourceForm = document.getElementById('update-resource-form');
const deleteResourceForm = document.getElementById('delete-resource-form');

const backendUrl = 'http://localhost:5000/resources'; // Adjust if your backend runs on a different port

async function fetchResources() {
    const response = await fetch(backendUrl);
    const resources = await response.json();
    displayResources(resources);
}

function displayResources(resources) {
    resourceList.innerHTML = '';
    resources.forEach(resource => {
        const div = document.createElement('div');
        div.classList.add('resource-item');
        div.innerHTML = `<span>ID: ${resource.id}</span><span>Name: ${resource.name}</span><span>Quantity: ${resource.quantity}</span>`;
        resourceList.appendChild(div);
    });
}

addResourceForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const quantity = parseInt(document.getElementById('quantity').value);
    const response = await fetch(backendUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, quantity }),
    });
    if (response.ok) {
        fetchResources();
        addResourceForm.reset();
    } else {
        alert('Failed to add resource');
    }
});

updateResourceForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('update-id').value;
    const name = document.getElementById('update-name').value;
    const quantity = document.getElementById('update-quantity').value ? parseInt(document.getElementById('update-quantity').value) : null;
    if (!id) return;
    const updateData = {};
    if (name) updateData.name = name;
    if (quantity !== null) updateData.quantity = quantity;

    const response = await fetch(`${backendUrl}/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updateData),
    });
    if (response.ok) {
        fetchResources();
        updateResourceForm.reset();
    } else {
        alert('Failed to update resource');
    }
});

deleteResourceForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('delete-id').value;
    if (!id) return;
    const response = await fetch(`${backendUrl}/${id}`, {
        method: 'DELETE',
    });
    if (response.ok) {
        fetchResources();
        deleteResourceForm.reset();
    } else {
        alert('Failed to delete resource');
    }
});

// Initial load of resources
fetchResources();