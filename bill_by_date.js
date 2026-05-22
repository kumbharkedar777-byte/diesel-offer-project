async function searchBillsByDate(){

    const fromDate =
    document.getElementById(
        "fromDate"
    ).value;

    const toDate =
    document.getElementById(
        "toDate"
    ).value;

    const response = await fetch(

        `http://127.0.0.1:5000/bills_by_date/${fromDate}/${toDate}`

    );

    const bills = await response.json();

    const tableBody =
    document.getElementById(
        "billTableBody"
    );

    tableBody.innerHTML = "";

    let totalFuel = 0;

    bills.forEach((bill)=>{

        totalFuel +=
        parseFloat(
            bill.fuel_liters
        );

        tableBody.innerHTML += `

        <tr>

            <td>${bill.id}</td>

            <td>${bill.mobile_number}</td>

            <td>${bill.vehicle_number}</td>

            <td>${bill.bill_number}</td>

            <td>${bill.fuel_liters}</td>

            <td>${bill.bill_date}</td>

        </tr>

        `;

    });

    document.getElementById(
        "totalFuel"
    ).innerText = totalFuel;

}