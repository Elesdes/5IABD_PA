document.addEventListener("DOMContentLoaded", function() {
    fetch('/api/get_profile')
    .then(response => response.json())
    .then(data => {
        let tableBody = document.getElementById("profile-form");
        data.forEach(profile => {
            let row = `
                <div class="row mb-3">
                    <label for="name" class="col-sm-2 col-form-label text-gray-800 dark:text-gray-100">Name</label>
                    <div class="col-sm-10">
                        <input type="text" class="form-control" id="name" name="name" placeholder="${profile.name}" value="${profile.name}">
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="forename" class="col-sm-2 col-form-label text-gray-800 dark:text-gray-100">Forename</label>
                    <div class="col-sm-10">
                        <input type="text" class="form-control" id="forename" name="forename" placeholder="${profile.forename}" value="${profile.forename}">
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="Email" class="col-sm-2 col-form-label text-gray-800 dark:text-gray-100">Email</label>
                    <div class="col-sm-10">
                        <input type="email" class="form-control" id="email" name="email" placeholder="${profile.email}" value="${profile.email}">
                    </div>
                </div>
                <div class="row mb-3">
                    <label for="password" class="col-sm-2 col-form-label text-gray-800 dark:text-gray-100">Change Password</label>
                    <div class="col-sm-10">
                        <input type="text" class="form-control" id="password" name="password">
                    </div>
                </div>
                <button type="submit" class="btn btn-primary text-gray-800 dark:text-gray-100">Send</button>
            `;
            tableBody.innerHTML += row;
        });
    });
});
