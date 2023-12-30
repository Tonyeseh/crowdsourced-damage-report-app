categoryName = document.getElementById("category-name")
categorySubmit = document.getElementById("submit-category")
alertBox = document.getElementById('information')
tbody = document.getElementById("table-body")
successModal = document.getElementById('successModal')
deleteButton = document.getElementById('deleteButton')

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
            if (data.status === 'success') {

              document.getElementById('successMessage').innerText = data.message
              $("#successModal").modal('show');

              tbody.innerHTML += `
                    <tr>
                      <td>
                        <div class="d-flex px-2 py-1">
                          <div class="d-flex flex-column justify-content-center">
                            <h6 class="mb-0 text-sm" id="cat-name-${data.data.id}" data-cat-name-${data.data.id}="${data.data.name}">${data.data.name}</h6>
                          </div>
                        </div>
                      </td>
                      <td class="align-middle text-center">
                        <p class="text-xs font-weight-bold mb-0">${data.data.damage_count || 0}</p>
                      </td>
                      <td class="align-middle text-center text-xs">
                        <span class="fw-bolder">0</span>
                      </td>
                      <td class="align-middle text-center">
                        <span class="text-secondary text-xs font-weight-bold">${data.data.created_at}</span>
                      </td>
                      <td class="align-middle text-center">
                        <a href="javascript:;" class="text-secondary font-weight-bold text-xs mx-2" data-cat-id=${data.data.id} data-toggle="tooltip" data-original-title="Edit Damage" onclick="editRecord(this)" data-bs-toggle="modal" data-bs-target="#editModal">
                          <i class="material-icons opacity-10">edit</i>
                        </a>
                        <a href="javascript:;" class="text-secondary text-xs text-danger mx-2" data-cat-id=${data.data.id} data-toggle="tooltip" data-original-title="Delete Location" onclick="deleteRecord(this)" data-bs-toggle="modal" data-bs-target="#deleteModal">
                            <i class="material-icons opacity-10">close</i>
                        </a>
                      </td>
                    </tr>
            `
            categoryName.value = ""
            }

            else {
              document.getElementById("failureMessage").innerText = data.message
              $("#failureModal").modal('show')
            }
        }) 
    }
})


editRecord = (elem) => {
  catId = elem.dataset.catId
  console.log(document.getElementById(`cat-name-${catId}`).innerText)

  document.getElementById("catName").value = document.getElementById(`cat-name-${catId}`).innerText

  document.getElementById('editButton').addEventListener('click', function editHandler (e) {
    e.preventDefault()

    if (document.getElementById("catName").value) {
      form = new FormData()
      form.append('name', document.getElementById("catName").value)
      fetch(`http://127.0.0.1:5001/api/v1/categories/${catId}`, {
        body: form,
        method: "PUT",
        headers: {
            Authorization: `Bearer ${getCookie('admin_access_token')}`
        }
      }).then(res => res.json())
      .then(data => {
        $("#editModal").modal('hide')
        
        if (data.status === "success") {
          document.getElementById("successMessage").innerText = data.message
          $("#successModal").modal('show')

          document.getElementById(`cat-name-${catId}`).innerText = data.data.name
        }
        else {
          document.getElementById("failureMessage").innerText = data.message
          $("#failureModal").modal('show')
        }
      })
    }
    document.getElementById('editButton').addEventListener('click', editHandler)
  })
}


function deleteRecord (elem) {
  $("#deleteModal").modal('show')
  catId = elem.dataset.catId
  deleteButton.setAttribute('data-id', catId)

  
  deleteButton.addEventListener('click', function deleteFunc (e) {
    e.preventDefault()
  
    fetch(`http://127.0.0.1:5001/api/v1/categories/${catId}`, {
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
        document.getElementById("failureMessage").innerText = data.message
        $("#failureModal").modal('show')
      }
    })
    deleteButton.removeEventListener('click', deleteFunc)
  })
}
