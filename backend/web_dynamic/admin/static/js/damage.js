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
            $("#editModal").modal('hide')
            if (data.status == "success") {
                document.getElementById('successMessage').innerText = data.message
                $("#successModal").modal('show');
                damageWorker.innerText = data.data.worker_name
                damageState.innerHTML = `<span class="badge badge-sm bg-gradient-info">${data.data.damage_state}</span>`
            }
            else {
                document.getElementById("failureMessage").innerText = data.message
                console.log(data.message)
                $("#failureModal").modal('show')
            }
        })
    }
    })
}
