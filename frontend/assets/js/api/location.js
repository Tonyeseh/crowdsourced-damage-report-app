locationName = document.getElementById("location-name")
locationSubmit = document.getElementById("submit-location")
tbody = document.getElementById("table-body")

window.onload = (e) => {
    console.log('fetching')
    tbody.innerHTML = ""
    fetch('http://127.0.0.1:5001/api/v1/locations')
    .then(res => res.json())
    .then(data => {
        data.forEach(item => {
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
        });
        console.log(data, tbody)})
}

function delete_location(event) {
    console.log(event)
}

locationSubmit.addEventListener('click', (e) => {
    e.preventDefault()

    locationNameVal = locationName.value

    if (locationNameVal.length > 5) {
        console.log('it would be sent')
        fetch('http://127.0.0.1:5001/api/v1/locations', {
            body: JSON.stringify({name: locationNameVal}),
            method: "POST",
            headers: {
                "Content-Type": "application/json",
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
                        <p class="text-xs font-weight-bold mb-0">1</p>
                      </td>
                      <td class="align-middle text-center text-sm">
                        <span class="badge badge-sm bg-gradient-success">75%</span>
                      </td>
                      <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${data.created_at}</span>
                      </td>
                      <td class="align-middle">
                        <a href="javascript:;" class="text-secondary font-weight-bold text-xs data-toggle="tooltip" data-original-title="Edit user">
                          Edit
                        </a>
                      </td>
                    <td class="align-middle">
                    <a href="javascript:;" class="text-secondary font-weight-bold text-xs text-danger" id=${data.id} data-toggle="tooltip" data-original-title="Delete Location onclick="delete_location(${data.id})">
                        Delete
                    </a>
                    </td>
                    </tr>
            `
            locationNameVal = ""
        }) 
    }
})