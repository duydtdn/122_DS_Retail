const swalWithBootstrapButtons = Swal.mixin({
  customClass: {
    confirmButton: 'btn btn-primary',
    cancelButton: 'btn btn-gray-50 ms-4'
  },
  buttonsStyling: false
});
const notyf = new Notyf({
  position: {
    x: 'right',
    y: 'top',
  },
  types: [
    {
      type: 'error',
      background: '#FA5252',
      icon: {
        className: 'fas fa-times',
        tagName: 'span',
        color: '#fff'
      },
      dismissible: false
    }
  ]
});