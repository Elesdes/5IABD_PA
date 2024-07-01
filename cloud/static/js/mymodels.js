document.addEventListener("DOMContentLoaded", function() {
    fetch('/api/get_mymodel')
    .then(response => response.json())
    .then(data => {
        let tableBody = document.getElementById("mymodel-table-body");
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
                    <td class="px-4 py-3">
                        <div class="flex items-center space-x-4 text-sm">
                            <button class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-purple-600 rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray" aria-label="Download" onclick="setMyModel('${model.idModel}')">
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"> 
                                    <circle cx="12" cy="12" r="10"/>
                                    <path d="M16 12l-4 4-4-4M12 8v7"/>
                                </svg>
                            </button>
                            <button class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-purple-600 rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray" aria-label="Delete" onclick="deleteMyModel('${model.idModel}')">
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

function deleteMyModel(idModel) {
    fetch(`/api/del_mymodels/?idModel=${idModel}`, {
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

function setMyModel(idModel) {
    fetch(`/api/take_mymodels/?idModel=${idModel}`, {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erreur lors de la mise à jour du modèle');
        }
        return response.json();
    })
    .then(data => {
        console.log('Modèle mise à jour avec succès:', data);
    })
    .catch(error => {
        console.error('Une erreur s\'est produite lors de la mise à jour du modèle:', error);
    }).finally(() => {
        window.location.reload();
    });
}
