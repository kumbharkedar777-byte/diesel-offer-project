const params = new URLSearchParams(window.location.search);

const id = params.get("id");

async function loadBill(){

    const response = await fetch(

        `http://127.0.0.1:5000/get_bill/${id}`

    );

    const bill = await response.json();

    document.getElementById("billId").value = bill.id;

    document.getElementById("mobile").value = bill.mobile_number;

    document.getElementById("vehicle").value = bill.vehicle_number;

    document.getElementById("bill").value = bill.bill_number;

    document.getElementById("liters").value = bill.fuel_liters;

    document.getElementById("date").value = bill.bill_date;

}

loadBill();
const form = document.getElementById("editForm");

form.addEventListener("submit", async function(event){

    event.preventDefault();

    const mobile =
        document.getElementById("mobile").value;

    const vehicle =
        document.getElementById("vehicle").value;

    const bill =
        document.getElementById("bill").value;

    const liters =
        document.getElementById("liters").value;

    const date =
        document.getElementById("date").value;

    const response = await fetch(

        `http://127.0.0.1:5000/update_bill/${id}`,

        {

            method: "PUT",

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

        }

    );

    const result = await response.json();

    alert(result.message);

    window.location.href = "bill_history.html";

});