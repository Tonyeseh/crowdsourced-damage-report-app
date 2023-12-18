firstName = document.getElementById('firstName')
lastName = document.getElementById('lastName')
emailAdd = document.getElementById('emailAdd')
password = document.getElementById('password')
confirmPassword = document.getElementById('confirmPassword')
submitBtn = document.getElementById('submit')

submitBtn.addEventListener('click', (e) => {
    e.preventDefault()

    if (firstName.value.length > 3 && lastName.value.length > 3 && emailAdd.value.length > 3 && password.value.length > 5 && password.value == confirmPassword.value) {
        form = new FormData()
        form.append('first_name', firstName.value)
        form.append('last_name', lastName.value)
        form.append('email', emailAdd.value)
        form.append('password', password.value)

        fetch('http://127.0.0.1:5001/api/v1/admin', {
            body: form,
            method: "POST",
        }).then(res => res.json())
        .then(data => {
            if (!data.error) {
                location = `sign-in.html`
            }
            console.log(data)
        })
        // firstName.value=""
        // lastName.value=""
        // emailAdd.value=""
        // password.value=""
        // confirmPassword.value=""
    }
})
