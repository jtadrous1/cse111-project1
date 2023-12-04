// this takes the user input and gets the data of the company
const form = document.getElementById("companyForm");
const resultDiv = document.getElementById("result");

form.addEventListener("submit", function (e) {
    e.preventDefault();
    const symbolInput = document.getElementById("symbol");
    const symbol = symbolInput.value.toUpperCase();

    // Redirect to the company_info page for the specified symbol
    window.location.href = `/company_info/${symbol}`;
});

// form.addEventListener("submit", function (e) {
//     e.preventDefault();
//     const symbolInput = document.getElementById("symbol");
//     const symbol = symbolInput.value.toUpperCase();

//     fetch(`/get_companies?symbol=${symbol}`)
//         .then(response => response.json())
//         .then(data => {
//             if (data.error) {
//                 resultDiv.innerHTML = `<p id="error">Error: ${data.error}</p>`;
//             } else {
//                 resultDiv.innerHTML = `
//                     <p>Company ID: ${data.CompanyID}</p>
//                     <p>Company Name: ${data.CompanyName}</p>
//                     <p>Stock Symbol: ${data.StockSymbol}</p>
//                     <p>Company Location: ${data.CompanyLocation}</p>
//                     <p>Industry: ${data.Industry}</p>
//                     <p>Sector: ${data.Sector}</p>
//                     <p>CEO: ${data.CEO}</p>
//                 `;
//             }
//         })
//         .catch(error => {
//             console.error(error);
//             resultDiv.innerHTML = "<p>An error occurred while fetching data.</p>";
//         });
// });