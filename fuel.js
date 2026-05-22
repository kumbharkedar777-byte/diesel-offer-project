async function searchFuelBills(){

    const mobile = document.getElementById(
        "mobileSearch"
    ).value;

    const response = await fetch(

        `http://127.0.0.1:5000/search_bills/${mobile}`

    );

    const bills = await response.json();

    const tableBody = document.getElementById(
        "fuelTableBody"
    );

    tableBody.innerHTML = "";

    bills.forEach(function(bill){

        const row = `

        <tr>

            <td>${bill.id}</td>

            <td>${bill.mobile_number}</td>

            <td>${bill.vehicle_number}</td>

            <td>${bill.bill_number}</td>

            <td>${bill.fuel_liters}</td>

            <td>${bill.bill_date}</td>

        </tr>

        `;

        tableBody.innerHTML += row;

    });

}