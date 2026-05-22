document.getElementById(
    "loginForm"
).addEventListener(

    "submit",

    async function(e){

        e.preventDefault();

        const loginData = {

            username:
            document.getElementById(
                "username"
            ).value,

            password:
            document.getElementById(
                "password"
            ).value

        };

        const response = await fetch(

            "http://127.0.0.1:5000/login",

            {

                method: "POST",

                headers: {

                    "Content-Type":
                    "application/json"

                },

                body: JSON.stringify(loginData)

            }

        );

        const result = await response.json();

        if(result.success){

         localStorage.setItem(

    "isLoggedIn",

    "true"

);

            alert("Login Successful!");

           

            window.location.href =
                "idx.html";

        }

        else{

            alert("Invalid Username or Password");

        }

    }

);