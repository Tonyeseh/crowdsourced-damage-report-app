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
//   
function updateRecord(elem) {
    statusCheckBox = elem.parentNode.previousSibling.previousSibling.childNodes[1].childNodes[1]
    
    form = new FormData()
    form.append('job_id', elem.id)
    form.append('status', statusCheckBox.checked)
    fetch('http://127.0.0.1:5001/api/v1/worker/damages/working_on', {
        body: form,
        method: 'POST',
        headers: {
            Authorization: `Bearer ${getCookie('worker_access_token')}`
        }
    }).then(res => res.json())
    .then(data => console.log(data))

}