selLocation = document.getElementById('location')
infras = document.getElementById('infras')
facilityName = document.getElementById('facility-name')
description = document.getElementById('description')
alertBox = document.getElementById('information')
submitBtn = document.getElementById('submit')
tbody = document.getElementById('table-body')


function getCookie(name) {
    // Split cookie string and get all individual name=value pairs in an array
    var cookieArr = document.cookie.split(";");
    
    // Loop through the array elements
    for(var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");
        
        /* Removing whitespace at the beginning of the cookie name
        and compare it with the given string */
        if(name == cookiePair[0].trim()) {
            // Decode the cookie value and return
            return decodeURIComponent(cookiePair[1]);
        }
    }
    
    // Return null if not found
    return null;
  }



selLocation.addEventListener('change', (e) => {
    infras.innerHTML = `
    <option selected>Pick an Infrastructure</option>`
    fetch(`http://127.0.0.1:5001/api/v1/locations/${selLocation.value}/infrastructures`, {
        headers: {
            Authorization: `Bearer ${getCookie('admin_access_token')}`
        }
    }).then(res => res.json())
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
            Authorization: `Bearer ${getCookie('admin_access_token')}`,
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
    alertBox.innerHTML += `
    <div class="alert alert-success alert-dismissible text-white" role="alert" id="alert">
    <span class="text-sm">${data.name} Added Successfully</span>
    <button type="button" class="btn-close text-lg py-3 opacity-10" data-bs-dismiss="alert" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
    </div>
    `
        })
    }
})


deleteRecord = (elem) => {
    facId = elem.dataset.facId
    deleteButton = document.getElementById('deleteButton')

    deleteButton.addEventListener('click', (e) => {
        e.preventDefault()

        fetch(`http://127.0.0.1:5001/api/v1/facilities/${facId}`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${getCookie('admin_access_token')}`
            }
        }).then(res => res.json())
        .then(data => {
            data.error || elem.parentNode.parentNode.remove()
        })
    })
}
