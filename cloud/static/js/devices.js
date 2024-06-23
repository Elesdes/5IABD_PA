document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/devices/link-device")
    .then((response) => response.json())
    .then((data) => {
      let tableBody = document.getElementById("device-table-body");
      data.forEach((device) => {
        let buttonHtml;
        if (device.IdUser) {
          buttonHtml = `<button class="bg-green-500 text-white font-bold py-2 px-4 rounded" disabled>Active</button>`;
        } else {
          buttonHtml = `<button class="bg-red-500 text-white font-bold py-2 px-4 rounded" onclick="confirmReconnectDevice('${device.IdDevice}')">Reconnect</button>`;
        }

        let row = `
                <tr class="text-gray-700 dark:text-gray-400" id="tabletr${device.IdDevice}">
                  <td class="px-4 py-3 text-sm">
                    <input class="form-control dark:bg-gray-800 dark:text-gray-200" type="text" value="${device.IdDevice}" readonly>
                  </td>
                  <td class="px-4 py-3 text-sm">
                    ${buttonHtml}
                  </td>
                  <td class="px-4 py-3 text-sm">
                    <button class="flex items-center justify-between px-2 py-2 text-sm font-medium leading-5 text-purple-600 rounded-lg dark:text-gray-400 focus:outline-none focus:shadow-outline-gray" aria-label="Delete" onclick="confirmRemoveDevice('${device.IdDevice}')">
                      <svg class="w-5 h-5" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                      </svg>
                    </button>
                  </td>
                </tr>
            `;
        tableBody.innerHTML += row;
      });
    });

  // Modal logic for removing device
  const confirmModal = document.getElementById("confirmModal");
  const confirmYes = document.getElementById("confirmYes");
  const confirmNo = document.getElementById("confirmNo");
  let deviceToRemove = null;

  function showRemoveModal(deviceId) {
    deviceToRemove = deviceId;
    confirmModal.classList.remove("hidden");
  }

  function hideRemoveModal() {
    confirmModal.classList.add("hidden");
    deviceToRemove = null;
  }

  confirmYes.addEventListener("click", function () {
    if (deviceToRemove) {
      let row = document.getElementById(`tabletr${deviceToRemove}`);
      row.remove();
      console.log(`Device ${deviceToRemove} removed.`);
      hideRemoveModal();
    }
  });

  confirmNo.addEventListener("click", function () {
    hideRemoveModal();
  });

  window.confirmRemoveDevice = function (deviceId) {
    showRemoveModal(deviceId);
  };

  // Modal logic for reconnecting device
  const reconnectModal = document.getElementById("reconnectModal");
  const reconnectYes = document.getElementById("reconnectYes");
  const reconnectNo = document.getElementById("reconnectNo");
  let deviceToReconnect = null;

  function showReconnectModal(deviceId) {
    deviceToReconnect = deviceId;
    reconnectModal.classList.remove("hidden");
  }

  function hideReconnectModal() {
    reconnectModal.classList.add("hidden");
    deviceToReconnect = null;
  }

  reconnectYes.addEventListener("click", function () {
    if (deviceToReconnect) {
      fetch(`/api/devices/link-device/${deviceToReconnect}`, {
        method: "GET",
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(`Device ${deviceToReconnect} reconnected:`, data);
          hideReconnectModal();
        })
        .catch((error) => {
          console.error("Error reconnecting device:", error);
          hideReconnectModal();
        });
    }
  });

  reconnectNo.addEventListener("click", function () {
    hideReconnectModal();
  });

  window.confirmReconnectDevice = function (deviceId) {
    showReconnectModal(deviceId);
  };
});

function reconnectDevice(deviceId) {
  fetch(`/api/devices/link-device/${deviceId}`, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(`Device ${deviceId} reconnected:`, data);
    })
    .catch((error) => {
      console.error("Error reconnecting device:", error);
    });
}
