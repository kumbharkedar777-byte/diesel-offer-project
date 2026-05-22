const form = document.getElementById("billForm");

form.addEventListener("submit", async function(event){

    event.preventDefault();

    // Capture values

    const mobile = document.getElementById("mobile").value;

    const vehicle = document.getElementById("vehicle").value;

    const bill = document.getElementById("bill").value;

    const liters = document.getElementById("liters").value;

    const date = document.getElementById("date").value;

    // Send data to Flask

    const response = await fetch("http://127.0.0.1:5000/save_bill", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            mobile,
            vehicle,
            bill,
            liters,
            date

        })

    });

    const result = await response.json();

    alert(result.message);

    form.reset();

});