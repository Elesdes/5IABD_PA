document.addEventListener("DOMContentLoaded", function() {
    fetch('/api/get_profile')
    .then(response => response.json())
    .then(data => {
        let tableBody = document.getElementById("profile-form");
        data.forEach(profile => {
            let row = `
                <div class="row mb-3">
                    <label for="name" class="col-sm-2 col-form-label">Name</label>
                    <div class="col-sm-10">
                        <input type="text" class="form-control" id="name" name="name" placeholder="${profile[1]}" value="${profile[1]}">
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="forename" class="col-sm-2 col-form-label">Forename</label>
                    <div class="col-sm-10">
                        <input type="text" class="form-control" id="forename" name="forename" placeholder="${profile[0]}" value="${profile[0]}">
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="Email" class="col-sm-2 col-form-label">Email</label>
                    <div class="col-sm-10">
                        <input type="email" class="form-control" id="email" name="email" placeholder="${profile[2]}" value="${profile[2]}">
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="password" class="col-sm-2 col-form-label">Change Password</label>
                    <div class="col-sm-10">
                        <input type="text" class="form-control" id="password" name="password">
                    </div>
                </div>
                <button type="submit" class="btn btn-primary">Send</button>
            `;
            tableBody.innerHTML += row;
        });
    });
});
