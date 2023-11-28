console.log("signing in page")

emailInput = document.getElementById("email")
passwordInput = document.getElementById("password")
submitBtn = document.getElementById("submit")

submitBtn.onclick = (e) => {
    e.preventDefault()

    if (emailInput.value && passwordInput.value) {
        fetch('http://127.0.0.1:5001/api/v1/auth/login').then((res => res.json())).then(data => console.log(data))
    }
}