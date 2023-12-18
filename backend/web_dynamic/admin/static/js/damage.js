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


function deleteRecord(element) {
    
    fetch(`http://127.0.0.1:5001/api/v1/damages/${element.id}`, {method: "DELETE", headers: {Authorization: `Bearer ${getCookie('admin_access_token')}`}}).then(res => res.json()).then(data => {

        data.error || element.parentNode.parentNode.remove()
    })
}

updateRecord = (element) => {
    workerId = element.parentNode.previousSibling.previousSibling.childNodes[1]

    if (workerId.value && element.id) {

    form = new FormData()
    form.append('damage_id', element.id)
    form.append('worker_id', workerId.value)

    fetch('http://127.0.0.1:5001/api/v1/damages/working_on', {
        body: form,
        method: 'POST',
        headers: {
            Authorization: `Bearer ${getCookie('admin_access_token')}`
        }
    }).then(res => res.json())
    .then(data => console.log(data))
}
}
