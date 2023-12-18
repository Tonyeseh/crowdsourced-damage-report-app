sel_location = document.getElementById('location')
infras_name = document.getElementById('infras-name')
description = document.getElementById('description')
tbody = document.getElementById("table-body")
alertBox = document.getElementById('information')
submitBtn = document.getElementById('submit')

window.onload = (e) => {
    console.log('getting locations')
    fetch('http://127.0.0.1:5001/api/v1/locations', {
        headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
        }
    })
    .then(res => res.json())
    .then(data => {
        data && data.forEach(item => {
            console.log(item)
            sel_location.innerHTML += `
            <option value="${item.id}">${item.name}</option>
            `
        });
    }).catch(e => {
        console.log(e)
    })
    fetch('http://127.0.0.0:5001/api/v1/infrastructures').then(res => {
        if (res.ok)
            return res.json()
        throw new Error('not found')
    })
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
                <p class="text-xs font-weight-bold mb-0 align-middle">${item.location_name}</p>
                </td>
                <td class="align-middle text-center text-sm">
                <span class="badge badge-sm bg-gradient-success">75%</span>
                </td>
                <td class="align-middle text-center">
                <span class="text-secondary text-xs font-weight-bold">${typeof item.created_at}</span>
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
}).catch(e => {
    console.log(e)
})
}

submitBtn.addEventListener('click', (e) => {
    console.log('submitting infras')
    if (sel_location.value && infras_name.value.length > 2 && description.value.length > 10){
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
            <p class="text-xs font-weight-bold mb-0 align-middle">${data.location_name}</p>
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
    alertBox.innerHTML += `
    <div class="alert alert-success alert-dismissible text-white" role="alert" id="alert">
    <span class="text-sm">${data.name} Added Successfully</span>
    <button type="button" class="btn-close text-lg py-3 opacity-10" data-bs-dismiss="alert" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
    </div>
    `
    description.value = ""
    infras_name.value = ""
    })
}
})