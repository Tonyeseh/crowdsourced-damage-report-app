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
    if (selLocation.value) {
        fetch(`http://127.0.0.1:5001/api/v1/locations/${selLocation.value}/infrastructures`, {
            headers: {
                Authorization: `Bearer ${getCookie('admin_access_token')}`
            }
        }).then(res => res.json())
        .then(data => {
            data.forEach(item => {
                infras.innerHTML += `
                <option value="${item.id}">${item.name}</option>
                `
            });
        })
    }
})

submitBtn.addEventListener('click', (e) => {
    e.preventDefault()

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
            if (data.status === 'success') {

              document.getElementById('successMessage').innerText = data.message
              $("#successModal").modal('show');
            
            tbody.innerHTML += `
        <tr>
            <td>
            <div class="d-flex px-2 py-1">
                <div class="d-flex flex-column justify-content-center">
                    <h6 class="mb-0 text-sm align-middle">${data.data.name}</h6>
                </div>
            </div>
            </td>
            <td>
                <p class="text-xs font-weight-bold mb-0 align-middle">${data.data.infrastructure_name}</p>
            </td>
            <td class="align-middle text-center text-xs">
                <span class="fw-bold">${data.data.location_name}</span>
            </td>
            <td class="align-middle text-center">
            <span class="text-secondary text-xs font-weight-bold">${data.data.created_at}</span>
            </td>
            <td class="align-middle text-center">
              <a href="javascript:;" class="text-secondary font-weight-bold text-xs mx-2" data-fac-id=${data.data.id} data-toggle="tooltip" data-original-title="Edit Damage" onclick="editRecord(this)" data-bs-toggle="modal" data-bs-target="#editModal">
                <i class="material-icons opacity-10">edit</i>
              </a>
              <a href="javascript:;" class="text-secondary text-xs text-danger mx-2" data-fac-id=${data.data.id} data-toggle="tooltip" data-original-title="Delete Location" onclick="deleteRecord(this)" data-bs-toggle="modal" data-bs-target="#deleteModal">
                  <i class="material-icons opacity-10">close</i>
              </a>
            </td>
        </tr>
    `
    }

    else {
      document.getElementById("failureMessage").innerText = data.message
      $("#failureModal").modal('show')
    }
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
            $("#deleteModal").modal('hide')
            if (data.status === 'success') {
                document.getElementById('successMessage').innerText = data.message
                $("#successModal").modal('show');

                elem.parentNode.parentNode.remove()
            }
            else {
                document.getElementById("failureMessage").innerText = data.message
                $("#failureModal").modal('show')
            }
        })
    })
}
