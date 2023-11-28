selLocation = document.getElementById('location')
selInfras = document.getElementById('infras')
selFacility = document.getElementById('facility')
category = document.getElementById('category')
description = document.getElementById('description')
otherFacility = document.getElementById('other-facility')
images = document.getElementById('images')
submitBtn = document.getElementById('submit')

// get the locations
console.log('getting locations')
fetch('http://127.0.0.1:5001/api/v1/locations')
.then(res => res.json())
.then(data => {
    data.forEach(item => {
        console.log(item)
        selLocation.innerHTML += `
        <option value="${item.id}">${item.name}</option>
        `
    });
})

fetch('http://127.0.0.1:5001/api/v1/categories')
.then(res => res.json())
.then(data => {
    data.forEach(item => {
        console.log(item)
        category.innerHTML += `
        <option value="${item.id}">${item.name}</option>
        `
    });
})

// getting the infrastructures
selLocation.addEventListener('change', (e) => {
    selInfras.innerHTML = `
        <option value="" selected>Pick an Infrastructure</option>
    `
    fetch(`http://127.0.0.1:5001/api/v1/locations/${selLocation.value}/infrastructures`).then(res => res.json())
    .then(data => {
        data.forEach(item => {
            console.log(item)
            selInfras.innerHTML += `
            <option value="${item.id}">${item.name}</option>
            `
        });
    })
})

// getting facilities
selInfras.addEventListener('change', e => {
    selFacility.innerHTML = `
        <option value="" selected>Pick an Infrastructure</option>
    `
    fetch(`http://127.0.0.1:5001/api/v1/infrastructures/${selInfras.value}/facilities`).then(res => res.json())
    .then(data => {
        data.forEach(item => {
            console.log(item)
            selFacility.innerHTML += `
            <option value="${item.id}">${item.name}</option>
            `
        });
        selFacility.innerHTML += ` <option value="others">Others</option>`
    })
})

selFacility.addEventListener('change', (e) => {
    if (selFacility.value == 'others') {
        otherFacility.innerHTML = `
        <label class="form-label">Facility Name</label>
        <input type="text" class="form-control" id="others-name">`
    }
    else {
        otherFacility.innerHTML = ""
    }
})

// submitting the damages
submitBtn.addEventListener('click', (e) => {
    otherNames = document.getElementById('others-name')
    if (otherNames || (selFacility.value !== 'others' && selFacility.value)) 
    if (category.value && selLocation.value && selInfras.value && selFacility.value && description.value.length > 5 && images.files) {
        form = new FormData()
        form.append('description', description.value)
        form.append('infras_name', selInfras.value)
        if (otherNames) {
            form.append('otherNames', otherNames.value)
        }
        for (i = 0; i < images.files.length; i++){
            form.append(`img-${i}`, images.files[i])
        }
        form.append('category_id', category.value)
        console.log(form)
        fetch(`http://127.0.0.0:5001/api/v1/facilities/${selFacility.value}/damages`, {
            body: form,
            method: "POST",
        })
        .then(res => res.json())
        .then(data => console.log(data))
        .catch(e => console.log(e))
        description.value=""
        console.log(images.files)
        while (images.files) {
            images.files.pop()
        }
    }
})


