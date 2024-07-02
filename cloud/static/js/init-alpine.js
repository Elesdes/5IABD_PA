function data() {
  function getThemeFromLocalStorage() {
    // if user already changed the theme, use it
    if (window.localStorage.getItem('dark')) {
      return JSON.parse(window.localStorage.getItem('dark'))
    }

    // else return their preferences
    return (
      !!window.matchMedia &&
      window.matchMedia('(prefers-color-scheme: dark)').matches
    )
  }

  function setThemeToLocalStorage(value) {
    window.localStorage.setItem('dark', value)
  }

  return {
    dark: getThemeFromLocalStorage(),
    toggleTheme() {
      this.dark = !this.dark
      setThemeToLocalStorage(this.dark)
    },
    isSideMenuOpen: false,
    toggleSideMenu() {
      this.isSideMenuOpen = !this.isSideMenuOpen
    },
    closeSideMenu() {
      this.isSideMenuOpen = false
    },
    isNotificationsMenuOpen: false,
    toggleNotificationsMenu() {
      this.isNotificationsMenuOpen = !this.isNotificationsMenuOpen
    },
    closeNotificationsMenu() {
      this.isNotificationsMenuOpen = false
    },
    isProfileMenuOpen: false,
    toggleProfileMenu() {
      this.isProfileMenuOpen = !this.isProfileMenuOpen
    },
    closeProfileMenu() {
      this.isProfileMenuOpen = false
    },
    isPagesMenuOpen: false,
    togglePagesMenu() {
      this.isPagesMenuOpen = !this.isPagesMenuOpen
    },
    // Modal
    isModalOpen: false,
    trapCleanup: null,
    openModal() {
      this.isModalOpen = true
      this.trapCleanup = focusTrap(document.querySelector('#modal'))
    },
    closeModal() {
      this.isModalOpen = false
      this.trapCleanup()
    },
    // Reconnect Modal
    isReconnectModalOpen: false,
    reconnectTrapCleanup: null,
    openReconnectModal(iddevice) {
      this.reconnectDeviceId = iddevice;
      this.isReconnectModalOpen = true
      this.reconnectTrapCleanup = focusTrap(document.querySelector('#reconnectModal'))
    },
    closeReconnectModal() {
      this.isReconnectModalOpen = false
      this.reconnectTrapCleanup()
    },
    reconnectDevice() {
      fetch(`/api/link-device/?device=${this.reconnectDeviceId}`, {
          method: 'POST'
      })
      .then(response => response.json())
      .then(data => {
          console.log('Success:', data);
      })
      .catch((error) => {
          console.error('Error:', error);
      });
      this.closeReconnectModal(); // Fermer la modal après l'action
    },
    // Delete Modal
    isDeleteModalOpen: false,
    deleteTrapCleanup: null,
    openDeleteModal() {
      this.isDeleteModalOpen = true
      this.deleteTrapCleanup = focusTrap(document.querySelector('#deleteModal'))
    },
    closeDeleteModal() {
      this.isDeleteModalOpen = false
      this.deleteTrapCleanup()
    },
  }
}
