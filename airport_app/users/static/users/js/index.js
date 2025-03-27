// Index javascript

// Ensure the DOM is loaded
document.addEventListener("DOMContentLoaded", function () {
    // Reference the necessary elements from the index.html file
    let name_searcher_origin = document.querySelector("#id_origin");
    let name_searcher_destination = document.querySelector("#id_destination");
    let list_origin = document.querySelector("#origin_suggestions");
    let list_destination = document.querySelector("#destination_suggestions");

    // FetchAirports function
    function fetchAirports(inputField, listElement) {
    // Get input then trim and lowercase it for easier searchability
        let query = inputField.value.trim().toLowerCase();

        // If the input field is empty
        if (!query) {
            listElement.innerHTML = "";
            listElement.style.border = "0px";
            return;
        }

        // Sending an AJAX request to django
        fetch(`/users/search-airports/?query=${query}`, {
            // Send an Ajax request
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(response => response.json())
        .then(data => {
            // Define Html variable
            let html = "";
            // If the length of the json file is greater than zero
            if (data.length > 0) {
                // We loop through all its elements and add them to the html variable as a list item
                data.forEach(airport => {
                    html += `<li onclick="selectAirport('${airport}', '${inputField.id}', '${listElement.id}')">${airport}</li>`;
                });
                listElement.style.border = "1px solid #ccc";
            } else {
                listElement.style.border = "0px";
            }
            // We pass the html variable to the html file
            listElement.innerHTML = html;
        })
        .catch(error => console.error("Error fetching airports:", error));
    }

    // We call the autocomplete function on the origin field
    name_searcher_origin.addEventListener("keyup", function() {
        fetchAirports(name_searcher_origin, list_origin);
    });

    // We call the autocomplete function on the destination field
    name_searcher_destination.addEventListener("keyup", function() {
        fetchAirports(name_searcher_destination, list_destination);
    });
});


// Make results clickable
function selectAirport(airportName, inputId, listId) {
    document.querySelector(`#${inputId}`).value = airportName;
    document.querySelector(`#${listId}`).innerHTML = "";
    document.querySelector(`#${listId}`).style.border = "0px";
}
