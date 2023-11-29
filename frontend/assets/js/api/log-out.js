logoutBtn = document.getElementById('logout')
signoutBtn = document.getElementById('sign-in')

function logout() {
    token = localStorage.removeItem('token')
    location = 'sign-in.html'
}

logoutBtn.onclick = logout
signoutBtn.onclick = logout
