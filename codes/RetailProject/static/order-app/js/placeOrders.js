const popupOrderDetail = () => {
  $('#order_detail_popup').modal({
    open: true,
    fadeDuration: 100,
    showClose: false,
    escapeClose: true,
    clickClose: true,
  })
}
const confirmCancelOrder = () => {
  $('#confirm_cancel_order_popup').modal({
    open: true,
    fadeDuration: 100,
    showClose: false,
    escapeClose: true,
    clickClose: true,
    // closeExisting: false
  })
}