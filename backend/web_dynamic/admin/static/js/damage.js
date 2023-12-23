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

function deleteHelper(elem) {
    deleteButton = document.getElementById('deleteButton')
    deleteButton.setAttribute('data-damage-id', elem.dataset.damageId)

    deleteButton.addEventListener('click', (e) => {
        e.preventDefault()
        
        fetch(`http://127.0.0.1:5001/api/v1/damages/${elem.dataset.damageId}`, {
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

function editRecord(elem) {
    workerSelect = document.getElementById('workerSelect')
    fetch(`http://127.0.0.1:5001/api/v1/damages/${elem.dataset.damageId}/workers`, {
        headers: {
            Authorization: `Bearer ${getCookie('admin_access_token')}`
        }
    }).then(res => res.json())
    .then(data => {
        workerSelect.innerHTML = `<option value="">Pick a worker...</option>`
        data.forEach(elem => {
            workerSelect.innerHTML += `<option value="${elem.id}">${elem.email}</option>`
        });
    })

    

    editButton = document.getElementById('editButton')
    damageRow = document.getElementById(elem.dataset.damageId)
    damageState = document.getElementById(`state-${elem.dataset.damageId}`)
    damageWorker = document.getElementById(`worker-${elem.dataset.damageId}`)
    editButton.addEventListener('click', (e) => {
        e.preventDefault()

        if (workerSelect.value) {

        form = new FormData()
        form.append('worker_id', workerSelect.value)

        fetch(`http://127.0.0.1:5001/api/v1/damages/${elem.dataset.damageId}`, {
            body: form,
            method: 'PUT',
            headers: {
                Authorization: `Bearer ${getCookie('admin_access_token')}`,
            }
        }).then(res => res.json())
        .then(data => {
            if (data.data) {
                damageWorker.innerText = data.data.worker_name
                damageState.innerHTML = `<span class="badge badge-sm bg-gradient-info">${data.data.damage_state}</span>`
            }
        })
        .catch(e => console.log(e))
    }
    })
}

// updateRecord = (element) => {
//     workerId = element.parentNode.previousSibling.previousSibling.childNodes[1]

//     if (workerId.value && element.id) {

//     form = new FormData()
//     form.append('damage_id', element.id)
//     form.append('worker_id', workerId.value)

//     fetch('http://127.0.0.1:5001/api/v1/damages/working_on', {
//         body: form,
//         method: 'POST',
//         headers: {
//             Authorization: `Bearer ${getCookie('admin_access_token')}`
//         }
//     }).then(res => res.json())
//     .then(data => console.log(data))
// }
// }
