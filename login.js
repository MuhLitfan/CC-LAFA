// Login form Starts
const loginOpnBtn = document.querySelector("#button-openform");
const loginBox = document.querySelector(".container-login");
const signupOpnBtn = document.querySelector(".button-login-signup");
const signupBox = document.querySelector(".container-signup");
const closebtn = document.querySelector(".closeButton");
const closebtnSignUp =document.querySelector(".closeButtonSignup");
const forgetPWLin =document.querySelector(".forgetPWLink");
const forgetP =document.querySelector(".forgetPW");
const closeButtonForgetP =document.querySelector(".closeButtonForgetPW")


loginOpnBtn.addEventListener("click", function () {
    if (loginBox.style.display === "none" || loginBox.style.display === "") {
        loginBox.style.display = "block";
    } else {
        loginBox.style.display = "none";
    }
});

signupOpnBtn.addEventListener("click", function (event) {
    event.preventDefault(); // Prevent form submission
    if (signupBox.style.display === "none" || signupBox.style.display === "") {
        signupBox.style.display = "block";
    } else {
        signupBox.style.display = "none";
    }
    loginBox.style.display = "none";
});


forgetPWLin.addEventListener("click", function (event) {
    event.preventDefault(); // Prevent form submission
    if (forgetP.style.display === "none" || forgetP.style.display === "") {
        forgetP.style.display = "block";
    } else {
        forgetP.style.display = "none";
    }
    loginBox.style.display = "none";
    signupBox.style.display = "none"
});

closebtn.addEventListener("click", function () {
    if(loginBox.style.display === "block")
    {
        loginBox.style.display = "none";
       
    }
})

closebtnSignUp.addEventListener("click", function(){
    if(signupBox.style.display === "block")
    {
        signupBox.style.display = "none";
    }
})

closeButtonForgetP.addEventListener("click", function(){
    if(forgetP.style.display === "block")
    {
        forgetP.style.display = "none";
    }
})
// Login Form Ends