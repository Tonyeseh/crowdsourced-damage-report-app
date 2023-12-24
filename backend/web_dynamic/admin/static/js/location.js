locationName = document.getElementById("location-name")
locationSubmit = document.getElementById("submit-location")
alertBox = document.getElementById('information')
tbody = document.getElementById("table-body")

locationName.value = ""

function delete_location(event) {
    console.log(event)
}

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

locationSubmit.addEventListener('click', (e) => {
    e.preventDefault()

    locationNameVal = locationName.value

    cookie = getCookie('admin_access_token')

    console.log(`Bearer ${cookie}`)

    if (locationNameVal.length > 5) {
        console.log('it would be sent')
        fetch('http://127.0.0.1:5001/api/v1/locations', {
            body: JSON.stringify({name: locationNameVal}),
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${cookie}`
              }
        }).then(res => res.json()).then(data => {
            console.log(data)
            tbody.innerHTML += `
            <tr>
                      <td>
                        <div class="d-flex px-2 py-1">
                          <div class="d-flex flex-column justify-content-center">
                            <h6 class="mb-0 text-sm">${data.name}</h6>
                          </div>
                        </div>
                      </td>
                      <td>
                        <p class="text-xs fw-bolder mb-0 text-center">0</p>
                      </td>
                      <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${data.created_at}</span>
                      </td>
                      <td class="align-middle text-center">
                        <a href="javascript:;" class="text-secondary font-weight-bold text-xs mx-2" data-location-id=${data.id} data-toggle="tooltip" data-original-title="Edit Location" onclick="editRecord(this)" data-bs-toggle="modal" data-bs-target="#editModal">
                          <i class="material-icons opacity-10">edit</i>
                        </a>
                        <a href="javascript:;" class="text-secondary text-xs text-danger mx-2" data-location-id=${data.id} data-toggle="tooltip" data-original-title="Delete Location" onclick="deleteRecord(this)" data-bs-toggle="modal" data-bs-target="#deleteModal">
                          <i class="material-icons opacity-10">close</i>
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

            locationName.value = ""
        }) 
    }
})


deleteRecord = (elem) => {
  locationId = elem.dataset.locationId
  deleteButton = document.getElementById('deleteButton')

  deleteButton.addEventListener('click', (e) => {
      e.preventDefault()

      fetch(`http://127.0.0.1:5001/api/v1/locations/${locationId}`, {
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
