if (localStorage.getItem('token')) {
    console.log(localStorage.getItem('item'))
}

emailInput = document.getElementById("email")
passwordInput = document.getElementById("password")
submitBtn = document.getElementById("submit")

submitBtn.onclick = (e) => {
    e.preventDefault()

    if (emailInput.value && passwordInput.value) {
        form = new FormData()

        form.append('email', emailInput.value)
        form.append('password', passwordInput.value)
        fetch('http://127.0.0.1:5001/api/v1/admin/login', {
            body: form,
            method: "POST"
        }).then((res => res.json())).then(data => {
            if (!data.error) {
            const token = data.data.token
            localStorage.setItem('token', token);
            location = 'dashboard.html'
            }
        })
    }
}