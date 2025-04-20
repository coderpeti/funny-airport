// Authentication javascript

// Ensure the DOM is loaded
document.addEventListener("DOMContentLoaded", function() {
   
    // LoadForm function
    function loadForm(formType) {
        // Sending an AJAX request to django
        fetch(`/users/authentication/${formType}/`, {
            // Send an Ajax request
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(response => response.json())
        .then(data => {
            // Paste the html received in the AJAX request into the html
            document.querySelector("#form-container").innerHTML = data.html;
            
            const form = document.querySelector("form")
            if (formType == "registration-login") {
                // Setting the action of the form to its own url
                form.action = "/users/authentication/registration/";
            } else if (formType == "login-registration") {
                // Setting the action of the form to its own url
                form.action = "/users/authentication/login/"
            }

            // Reattach the function responsible for submitting the form, because the original form's event listener is lost with AJAX loading
            form.addEventListener("submit", submitForm)
        })
        .catch(error => console.error("Error loading form", error));

        // Add the active class to the active loaded form
        document.querySelector("#toggle-register").classList.toggle("active", formType === "registration-login");
        document.querySelector("#toggle-login").classList.toggle("active", formType === "login-registration");
    }
    
    
    // SubmitForm function
    function submitForm(event) {
        // Prevent the form from being sent by reloading the entire page
        event.preventDefault();

        let form = event.target;
        // Gathering the form's input data
        let formData = new FormData(form);
        // If action is set, the url points to that page instead of the current one
        let url = form.action
        
        fetch(url, {
            method: "POST",
            // Body of the request that contains the data
            body: formData,
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(response => response.json())
        .then(data => {
            // If the operation is successfull
            if (data.success) {
                window.location.href = data.redirect;
            } else {
                // Insert new html content
                document.querySelector("#form-container").innerHTML = data.html;
                // Reattach the function responsible for submitting the form, because the original form's event listener is lost with AJAX loading
                document.querySelector("form").addEventListener("submit", submitForm);
            }
        })
        // Handle errors
        .catch(error => console.error("Error submitting form:", error));
    }

    document.querySelector("form").addEventListener("submit", submitForm);
    // Make the loadForm function available to other files
    window.loadForm = loadForm;
})   

