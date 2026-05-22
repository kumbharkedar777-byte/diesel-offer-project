document.getElementById(
    "redeemForm"
).addEventListener(

    "submit",

    async function(e){

        e.preventDefault();

        const mobileNumber =
        document.getElementById(
            "mobileNumber"
        ).value;

        const response = await fetch(

            `http://127.0.0.1:5000/redeem_offer/${mobileNumber}`,

            {

                method: "POST"

            }

        );

        const result =
        await response.json();

        alert(result.message);

        document.getElementById(
            "redeemForm"
        ).reset();

    }

);