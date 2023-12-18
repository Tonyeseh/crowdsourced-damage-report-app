selLocation = document.getElementById('location')
infras = document.getElementById('infras')
facilityName = document.getElementById('facility-name')
description = document.getElementById('description')
submitBtn = document.getElementById('submit')
tbody = document.getElementById('table-body')
console.log("wheew")


console.log("getting facilities")
fetch('http://127.0.0.1:5001/api/v1/facilities')
.then(res => res.json())
.then(data => {console.log(data)
   data.error || data.forEach(item => {
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
        <a href="javascript:;" class="text-secondary font-weight-bold text-xs text-danger" id=${item.id} data-toggle="tooltip" data-original-title="Delete Location" onclick="deleteRecord(this)">
            Delete
        </a>
        </td>
    </tr>
`
   })
})


    console.log('getting locations')
    fetch('http://127.0.0.1:5001/api/v1/locations', {
        headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
        }
    })
    .then(res => res.json())
    .then(data => {
        data.forEach(item => {
            console.log(item)
            selLocation.innerHTML += `
            <option value="${item.id}">${item.name}</option>
            `
        });
    })


selLocation.addEventListener('change', (e) => {
    infras.innerHTML = `
    <option selected>Pick an Infrastructure</option>`
    fetch(`http://127.0.0.1:5001/api/v1/locations/${selLocation.value}/infrastructures`).then(res => res.json())
    .then(data => {
        data.forEach(item => {
            console.log(item)
            infras.innerHTML += `
            <option value="${item.id}">${item.name}</option>
            `
        });
    })
})

submitBtn.addEventListener('click', (e) => {
    e.preventDefault()

    console.log('submitting')
    if (selLocation.value && infras.value && facilityName.value.length > 3 && description.value) {
        fetch(`http://127.0.0.0:5001/api/v1/infrastructures/${infras.value}/facilities`, {
            body: JSON.stringify({name: facilityName.value, description: description.value}),
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
            <a href="javascript:;" class="text-secondary font-weight-bold text-xs text-danger" id=${data.id} data-toggle="tooltip" data-original-title="Delete Location" onclick="deleteRecord(this)">
                Delete
            </a>
            </td>
        </tr>
    `
        })
    }
})

function deleteRecord(element) {
    
    fetch(`http://127.0.0.1:5001/api/v1/facilities/${element.id}`, {method: "DELETE"}).then(res => res.json()).then(data => {

        data.error || element.parentNode.parentNode.remove()
    })
}

