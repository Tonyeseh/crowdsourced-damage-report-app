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


function verifyJob(elem) {
    verify = document.getElementById('verify')

    damage_id = location.pathname.split('/')[2]
    console.log(elem)

    console.log(verify.value)

    if (verify.value) {

        form = new FormData()
        form.append('damage_id', damage_id)
        form.append('verify', verify.value)

        fetch('http://127.0.0.1:5001/api/v1/users/verify', {
            body: form,
            method: "POST",
            headers: {
                Authorization: `Bearer ${getCookie('user_access_token')}`
            }
        }).then(res => res.json())
        .then(data => console.log(data))
        .catch(err => console.log(`error ${err}`))
    }
}
