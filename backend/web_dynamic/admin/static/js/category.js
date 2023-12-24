categoryName = document.getElementById("category-name")
categorySubmit = document.getElementById("submit-category")
alertBox = document.getElementById('information')
tbody = document.getElementById("table-body")

categoryName.value = ""

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



categorySubmit.addEventListener('click', (e) => {
    e.preventDefault()

    categoryNameVal = categoryName.value

    if (categoryNameVal.length > 5) {
        console.log('it would be sent')
        fetch('http://127.0.0.1:5001/api/v1/categories', {
            body: JSON.stringify({name: categoryNameVal}),
            method: "POST",
            headers: {
              Authorization: `Bearer ${getCookie('admin_access_token')}`,
              "Content-Type": "application/json",
              }
        }).then(res => res.json()).then(data => {
            if (!data.error){
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
                        <p class="text-xs font-weight-bold mb-0">${data.damage_count || 0}</p>
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
            alertBox.innerHTML += `
            <div class="alert alert-success alert-dismissible text-white" role="alert" id="alert">
            <span class="text-sm">${data.name} Added Successfully</span>
            <button type="button" class="btn-close text-lg py-3 opacity-10" data-bs-dismiss="alert" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
            </div>
            `

            categoryName.value = ""
            }
        }) 
    }
})



deleteRecord = (elem) => {
  catId = elem.dataset.catId
  deleteButton = document.getElementById('deleteButton')

  deleteButton.addEventListener('click', (e) => {
      e.preventDefault()

      fetch(`http://127.0.0.1:5001/api/v1/categories/${catId}`, {
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

