document.getElementById(
    "userForm"
).addEventListener(

    "submit",

    async function(e){

        e.preventDefault();

        const userData = {

            full_name:
            document.getElementById(
                "fullName"
            ).value,

            mobile_number:
            document.getElementById(
                "mobileNumber"
            ).value,

            username:
            document.getElementById(
                "username"
            ).value,

            password:
            document.getElementById(
                "password"
            ).value,

            role:
            document.getElementById(
                "role"
            ).value

        };

        const response = await fetch(

            "http://127.0.0.1:5000/add_user",

            {

                method: "POST",

                headers: {

                    "Content-Type":
                    "application/json"

                },

                body: JSON.stringify(userData)

            }

        );

        const result = await response.json();

        alert(result.message);

        document.getElementById(
            "userForm"
        ).reset();

    }

);