function login() {
    document.getElementById("load").classList.add("active");
    let button = document.getElementById("login-button");
    button.classList.add("disabled");

    var formElement = document.getElementById("login-form");
    
    req = new XMLHttpRequest();

    //check login response
    req.onreadystatechange = () => {
        if (req.readyState === 4) {
            console.log(req.response, req.status);
            if (req.status == 200) {
                window.location.replace("/");
            } else {
                alert(req.response + " - " + String(req.status));
                document.getElementById("load").classList.remove("active");
                button.classList.remove("disabled");
            }
        }
    }
    
    req.open("POST", "/login");
    req.send(new FormData(formElement));
}

function register() {
    document.getElementById("load").classList.add("active");
    let button = document.getElementById("login-button");
    button.classList.add("disabled");

    var formElement = document.getElementById("register-form");
    
    req = new XMLHttpRequest();

    //check login response
    req.onreadystatechange = () => {
        if (req.readyState === 4) {
            console.log(req.response, req.status);
            if (req.status == 200) {
                window.location.replace("/");
            } else {
                alert(req.response + " - " + String(req.status));
                document.getElementById("load").classList.remove("active");
                button.classList.remove("disabled");
            }
        }
    }
    
    req.open("POST", "/register");
    req.send(new FormData(formElement));
}