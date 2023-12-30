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

function confirmStatus(elem) {
    workId = elem.dataset.workId
    submitStatus = document.getElementById('workStatus')
    submitStatus.setAttribute('data-work-id', workId)
}


function updateStatus(elem) {
    workId = elem.dataset.workId
    console.log(workId)
    
    form = new FormData()
    form.append('job_id', workId)
    form.append('status', true)
    fetch('http://127.0.0.1:5001/api/v1/worker/damages/working_on', {
        body: form,
        method: 'POST',
        headers: {
            Authorization: `Bearer ${getCookie('worker_access_token')}`
        }
    }).then(res => res.json())
    .then(data => {
        console.log(data)
        $('#doneModal').modal('hide')
        if (data.status == "success") {
            document.getElementById('successMessage').innerText = data.message
            $("#successModal").modal('show');
            document.getElementById(`job-${workId}`).remove()
        }
        else {
            document.getElementById("failureMessage").innerText = data.message
            $("#failureModal").modal('show')
        }

    })


}