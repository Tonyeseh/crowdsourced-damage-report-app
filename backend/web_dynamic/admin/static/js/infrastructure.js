sel_location = document.getElementById('location')
infras_name = document.getElementById('infras-name')
description = document.getElementById('description')
tbody = document.getElementById("table-body")
alertBox = document.getElementById('information')
submitBtn = document.getElementById('submit')


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


submitBtn.addEventListener('click', (e) => {
    console.log('submitting infras')
    if (sel_location.value && infras_name.value.length > 2 && description.value.length > 10){
        console.log(sel_location.value)
    fetch(`http://127.0.0.0:5001/api/v1/locations/${sel_location.value}/infrastructures`, {
        body: JSON.stringify({name: infras_name.value, description: description.value}),
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
            <td class="text-xs font-weight-bold mb-0 align-middle">
                ${data.data.location_name}
            </td>
            <td class="align-middle text-center text-xs">
            <span class="fw-bold">0</span>
            </td>
            <td class="align-middle text-center">
            <span class="text-secondary text-xs font-weight-bold">${data.data.created_at}</span>
            </td>
            <td class="align-middle text-center">
            <a href="javascript:;" class="text-secondary font-weight-bold text-xs mx-2" data-infras-id=${data.id} data-toggle="tooltip" data-original-title="Edit Infrastructure" onclick="editRecord(this)" data-bs-toggle="modal" data-bs-target="#editModal">
                            <i class="material-icons opacity-10">edit</i>
                          </a>
                          <a href="javascript:;" class="text-secondary text-xs text-danger mx-2" data-infras-id=${data.id} data-toggle="tooltip" data-original-title="Delete Infrastructure" onclick="deleteRecord(this)" data-bs-toggle="modal" data-bs-target="#deleteModal">
                              <i class="material-icons opacity-10">close</i>
                          </a>
            </td>
        </tr>
    `
    description.value = ""
    infras_name.value = ""
    }

    else {
        document.getElementById("failureMessage").innerText = data.message
        $("#failureModal").modal('show')
    }
    })
}
})


deleteRecord = (elem) => {
    infrasId = elem.dataset.infrasId
    deleteButton = document.getElementById('deleteButton')

    deleteButton.addEventListener('click', (e) => {
        e.preventDefault()

        fetch(`http://127.0.0.1:5001/api/v1/infrastructures/${infrasId}`, {
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
                $("#failureMessage").innerText = data.message
                $("#failureModal").modal('show')
            }
        })
    })
}
