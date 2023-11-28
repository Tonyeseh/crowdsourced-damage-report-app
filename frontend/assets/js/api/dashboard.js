totalDamage = document.getElementById('total-report')
completedDamage = document.getElementById('completed-report')
reviewDamage = document.getElementById('review-report')
assignedDamage = document.getElementById('assigned-report')
tableBody = document.getElementById('tbody')
tableBody.innerHTML = ""

window.onload = (e) => {
    fetch('http://127.0.0.1:5001/api/v1/damages/info')
    .then(res => res.json())
    .then(data => {
        console.log(data)
        totalDamage.innerText = data.all
        completedDamage.innerText = data.completed
        reviewDamage.innerText = data.in_review
        assignedDamage.innerText = data.assigned
        data.locations.forEach(element => {
            console.log(element)
            tableBody.innerHTML += `<tr>
            <td>
              <div class="d-flex px-2 py-1">
                
                <div class="d-flex flex-column justify-content-center">
                  <h6 class="mb-0 text-sm">${element.name}</h6>
                </div>
              </div>
            </td>
            <td class="align-middle text-center text-sm">
            <span class="text-xs font-weight-bold"> ${element.damage_count} </span>
            </td>
            <td class="align-middle text-center text-sm">
              <span class="text-xs font-weight-bold"> ${element.cost || "Not valued"} </span>
            </td>
            <td class="align-middle text-center text-sm">
            <span class="text-xs font-weight-bold"> ${element.completed || 0} </span>
            </td>
          </tr>`
        });
    })
}
