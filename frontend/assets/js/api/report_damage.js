selLocation = document.getElementById('location')
selInfras = document.getElementById('infras')
selFacility = document.getElementById('facility')
description = document.getElementById('description')
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
        <option value"" selected>Pick an Infrastructure</option>
    `
    fetch(`http://127.0.0.1:5001/api/v1/infrastructures/${selInfras.value}/facilities`).then(res => res.json())
    .then(data => {
        data.forEach(item => {
            console.log(item)
            selFacility.innerHTML += `
            <option value="${item.id}">${item.name}</option>
            `
        });
    })
})

// submitting the damages
submitBtn.addEventListener('click', (e) => {
    if (selLocation.value && selInfras.value && selFacility.value && description.value.length > 5 && images.files) {
        form = new FormData()
        form.append('description', JSON.stringify(description.value))
        for (i = 0; i < images.files.length; i++){
            form.append(`img-${i}`, images.files[i])
        }
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
