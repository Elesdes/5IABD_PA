document.addEventListener("DOMContentLoaded", function() {
    fetch('/api/get_models')
    .then(response => response.json())
    .then(data => {
        let tableBody = document.getElementById("model-table-body");
        data.forEach(model => {
            let row = `
                <tr class="text-gray-700 dark:text-gray-400" id="tabletr${model.idModel}">
                    <td class="px-4 py-3" id="idModel${model.idModel}">
                        ${model.idModel}
                    </td>
                    <td class="px-4 py-3">
                        <div class="flex items-center text-sm">
                            <div>
                                <p class="font-semibold"><input type="text" value="${model.path}"></p></p>
                            </div>
                        </div>
                    </td>
                    <td class="px-4 py-3 text-sm">
                        <input type="text" value="${model.date}">
                    </td>
                    <td class="px-4 py-3 text-xs">
                        <span class="px-2 py-1 font-semibold leading-tight rounded-full">
                            <input type="text" value="${model.idUsers}">
                        </span>
                    </td>
                    <td class="px-4 py-3">
                        <div class="flex items-center space-x-4 text-sm">
                            <button class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-purple-600 rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray" aria-label="Edit" onclick="editModel('${encodeURIComponent(JSON.stringify(model))}')">
                                <svg class="w-5 h-5" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"></path>
                                </svg>
                            </button>
                            <button class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-purple-600 rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray" aria-label="Delete" onclick="deleteModel('${model.idUsers}','${model.idModel}')">
                                <svg class="w-5 h-5" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                                </svg>
                            </button>
                        </div>
                    </td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    });
});

function editModel(model) {
    model = decodeURIComponent(model)
    model = JSON.parse(model)
    let tabletrIdModel = "#tabletr" + model.idModel
    let inputValues = $(tabletrIdModel).find("input").map(function() {
        return $(this).val();
    }).get();
    let selectValues = $(tabletrIdModel).find("select").map(function() {
        return $(this).val();
    }).get();
    fetch(`/api/update_model/?idModel=${model.idModel}&path=${inputValues[0]}&date=${inputValues[1]}&idUsers=${inputValues[2]}`, {
        method: 'POST'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erreur lors de l\'édition du modèle');
        }
        return response.json();
    })
    .then(data => {
        console.log('Modèle édité avec succès:', data);
    })
    .catch(error => {
        console.error('Une erreur s\'est produite lors de l\'édition du modèle:', error);
    }).finally(() => {
        window.location.reload();
    });
}

function deleteModel(idUsers, idModel) {
    fetch(`/api/del_models/?idUsers=${idUsers}&idModel=${idModel}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erreur lors de la suppression du modèle');
        }
        return response.json();
    })
    .then(data => {
        console.log('Modèle supprimé avec succès:', data);
    })
    .catch(error => {
        console.error('Une erreur s\'est produite lors de la suppression du modèle:', error);
    }).finally(() => {
        window.location.reload();
    });
}
