sel_location = document.getElementById('location')
infras_name = document.getElementById('infras-name')
description = document.getElementById('description')
tbody = document.getElementById("table-body")
submitBtn = document.getElementById('submit')

window.onload = (e) => {
    console.log('getting locations')
    fetch('http://127.0.0.1:5001/api/v1/locations')
    .then(res => res.json())
    .then(data => {
        data.forEach(item => {
            console.log(item)
            sel_location.innerHTML += `
            <option value="${item.id}">${item.name}</option>
            `
        });
    })
    fetch('http://127.0.0.0:5001/api/v1/infrastructures').then(res => res.json())
    .then(data => {
        data.forEach(item => {
            console.log(data)
            tbody.innerHTML += `
            <tr>
                <td>
                <div class="d-flex px-2 py-1">
                    <div class="d-flex flex-column justify-content-center">
                    <h6 class="mb-0 text-sm align-middle">${item.name}</h6>
                    </div>
                </div>
                </td>
                <td>
                <p class="text-xs font-weight-bold mb-0 align-middle">1</p>
                </td>
                <td class="align-middle text-center text-sm">
                <span class="badge badge-sm bg-gradient-success">75%</span>
                </td>
                <td class="align-middle text-center">
                <span class="text-secondary text-xs font-weight-bold">${item.created_at}</span>
                </td>
                <td class="align-middle">
                <a href="javascript:;" class="text-secondary font-weight-bold text-xs" data-toggle="tooltip" data-original-title="Edit user">
                    Edit
                </a>
                </td>
                <td class="align-middle">
                <a href="javascript:;" class="text-secondary font-weight-bold text-xs text-danger" id=${item.id} data-toggle="tooltip" data-original-title="Delete Location" onclick="delete_location(${item.id})">
                    Delete
                </a>
                </td>
            </tr>
        `
})
})
}

submitBtn.addEventListener('click', (e) => {
    console.log('submitting infras')
    if (sel_location.value && infras_name.value.length > 5 && description.value.length > 10){
        console.log(sel_location.value)
    fetch(`http://127.0.0.0:5001/api/v1/locations/${sel_location.value}/infrastructures`, {
        body: JSON.stringify({name: infras_name.value, description: description.value}),
        method: "POST",
        headers: {
            "Content-Type": "application/json",
          }
    })
    .then(res => res.json())
    .then(data => {
        tbody.innerHTML += `
        <tr>
            <td>
            <div class="d-flex px-2 py-1">
                <div class="d-flex flex-column justify-content-center">
                <h6 class="mb-0 text-sm align-middle">${data.name}</h6>
                </div>
            </div>
            </td>
            <td>
            <p class="text-xs font-weight-bold mb-0 align-middle">1</p>
            </td>
            <td class="align-middle text-center text-sm">
            <span class="badge badge-sm bg-gradient-success">75%</span>
            </td>
            <td class="align-middle text-center">
            <span class="text-secondary text-xs font-weight-bold">${data.created_at}</span>
            </td>
            <td class="align-middle">
            <a href="javascript:;" class="text-secondary font-weight-bold text-xs" data-toggle="tooltip" data-original-title="Edit user">
                Edit
            </a>
            </td>
            <td class="align-middle">
            <a href="javascript:;" class="text-secondary font-weight-bold text-xs text-danger" id=${data.id} data-toggle="tooltip" data-original-title="Delete Location" onclick="delete_location(${data.id})">
                Delete
            </a>
            </td>
        </tr>
    `
    })
}
})