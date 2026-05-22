async function loadRedeemReports(){

    const response = await fetch(

        "http://127.0.0.1:5000/redeem_reports"

    );

    const reports =
    await response.json();

    const tableBody =
    document.getElementById(
        "redeemTableBody"
    );

    tableBody.innerHTML = "";

    reports.forEach((report)=>{

        tableBody.innerHTML += `

        <tr>

            <td>${report.id}</td>

            <td>${report.mobile_number}</td>

            <td>${report.total_fuel}</td>

            <td>${report.reward_name}</td>

            <td>${report.redeemed_date}</td>

        </tr>

        `;

    });

}

loadRedeemReports();