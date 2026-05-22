document.getElementById(
    "passwordForm"
).addEventListener(

    "submit",

    async function(e){

        e.preventDefault();

        const passwordData = {

            username:
            document.getElementById(
                "username"
            ).value,

            old_password:
            document.getElementById(
                "oldPassword"
            ).value,

            new_password:
            document.getElementById(
                "newPassword"
            ).value

        };

        const response = await fetch(

            "http://127.0.0.1:5000/change_password",

            {

                method: "PUT",

                headers: {

                    "Content-Type":
                    "application/json"

                },

                body: JSON.stringify(
                    passwordData
                )

            }

        );

        const result =
        await response.json();

        alert(result.message);

        document.getElementById(
            "passwordForm"
        ).reset();

    }

);