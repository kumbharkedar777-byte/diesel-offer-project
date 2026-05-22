async function loadOfferAchievers(){

    const response = await fetch(

        "http://127.0.0.1:5000/offer_achievers"

    );

    const achievers =
    await response.json();

    const tableBody =
    document.getElementById(
        "offerTableBody"
    );

    tableBody.innerHTML = "";

    achievers.forEach((customer)=>{

        tableBody.innerHTML += `

        <tr>

            <td>
                ${customer.mobile_number}
            </td>

            <td>
                ${customer.total_fuel}
            </td>

            <td>

                <span class="badge bg-success">

                    Eligible

                </span>

            </td>

        </tr>

        `;

    });

}

loadOfferAchievers();