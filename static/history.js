async function loadBills(){

    const response = await fetch(
        "http://127.0.0.1:5000/get_bills"
    );

    const bills = await response.json();

    const tableBody = document.getElementById(
        "historyTableBody"
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

            <td>

                <button
                    class="btn btn-warning btn-sm"
                    onclick="editBill(${bill.id})">

                    Edit

                </button>

                <button
                    class="btn btn-danger btn-sm ms-2"
                    onclick="deleteBill(${bill.id})">

                    Delete

                </button>

            </td>

        </tr>

        `;

        tableBody.innerHTML += row;

    });

}

function editBill(id){

    window.location.href =
        `edit_bill.html?id=${id}`;

}

async function deleteBill(id){

    const confirmDelete = confirm(
        "Are you sure you want to delete this bill?"
    );

    if(!confirmDelete){

        return;

    }

    const response = await fetch(

        `http://127.0.0.1:5000/delete_bill/${id}`,

        {

            method: "DELETE"

        }

    );

    const result = await response.json();

    alert(result.message);

    loadBills();

}
async function searchBills(){

    const mobile = document.getElementById(
        "searchMobile"
    ).value;

    const response = await fetch(

        `http://127.0.0.1:5000/search_bills/${mobile}`

    );

    const bills = await response.json();

    const tableBody = document.getElementById(
        "historyTableBody"
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

            <td>

                <button
                    class="btn btn-warning btn-sm"
                    onclick="editBill(${bill.id})">

                    Edit

                </button>

                <button
                    class="btn btn-danger btn-sm ms-2"
                    onclick="deleteBill(${bill.id})">

                    Delete

                </button>

            </td>

        </tr>

        `;

        tableBody.innerHTML += row;

    });

}

loadBills();
async function downloadPDF(){

    const { jsPDF } = window.jspdf;

    const doc = new jsPDF();

    const response = await fetch(

        "http://127.0.0.1:5000/get_bills"

    );

    const bills = await response.json();

    const tableData = [];

    bills.forEach((bill)=>{

        tableData.push([

            bill.id,
            bill.mobile_number,
            bill.vehicle_number,
            bill.bill_number,
            bill.fuel_liters,
            bill.bill_date

        ]);

    });

    doc.text(

        "Diesel Offer Bill Report",

        14,

        15

    );

    doc.autoTable({

        head:[[
            "ID",
            "Mobile",
            "Vehicle",
            "Bill No",
            "Liters",
            "Date"
        ]],

        body: tableData,

        startY:25

    });

    doc.save(
        "bill_report.pdf"
    );

}