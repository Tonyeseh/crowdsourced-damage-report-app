tbody = document.getElementById('table-body')

// fetching damages
console.log("fetching damages")
fetch('http://127.0.0.1:5001/api/v1/damages')
.then(res => res.json())
.then(data => {
    console.log(data)
    data.error || data.forEach(item => {
        tbody.innerHTML += `
        <tr>
            <td>
            <div class="d-flex px-2 py-1">
                <div class="d-flex flex-column justify-content-center">
                <h6 class="mb-0 text-sm align-middle">${item.facility_name} in ${item.infrastructure_name}</h6>
                </div>
            </div>
            </td>
            <td>
            <p class="text-xs font-weight-bold mb-0 align-middle">${item.priority}</p>
            </td>
            <td class="align-middle text-center text-sm">
            <span class="badge badge-sm bg-gradient-success">${item.state}</span>
            </td>
            <td class="align-middle text-center">
            <span class="text-secondary text-xs font-weight-bold">${item.created_at}</span>
            </td>
            <td class="align-middle">
            <a href="javascript:;" class="text-secondary font-weight-bold text-xs" data-toggle="tooltip" data-original-title="Edit user">
                View
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

function deleteRecord(element) {
    
    fetch(`http://127.0.0.1:5001/api/v1/damages/${element.id}`, {method: "DELETE"}).then(res => res.json()).then(data => {

        data.error || element.parentNode.parentNode.remove()
    })
}


console.log("damages yeeee")

