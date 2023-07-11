let orderList = [];
const popupOrderDetail = (orderId) => {
  renderOrderDetail(orderId);
  $('#order_detail_popup').modal({
    open: true,
    fadeDuration: 100,
    showClose: true,
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
const renderOrderDetail = (id) => {
  const itemDetail = orderList.find(order => order.id==id)
  const stringHtml = `
  <div class="container">
      <div class="row">
        <div class="col-md-offset-3">
          <h1 class="text-center font-weight-bold">Chi tiết đơn hàng</h1>
          <div class="row mb-1 ">
            <span class="col-4">Mã ĐH:</span>
            <span class="col-8 fst-italic fw-bold">${itemDetail.id}</span>
          </div>
          <div class="row mb-1 ">
            <span class="col-4">Ngày tạo:</span>
            <span class="col-8 fst-italic">${new Date(itemDetail.order_date).toLocaleDateString()}</span>
          </div>
          <div class="row mb-1 ">
            <span class="col-4">Số ĐT:</span>
            <span class="col-8 fst-italic">0928201102</span>
          </div>
          <div class="row mb-1 ">
            <span class="col-4">Trạng thái:</span>
            <span class="col-8 fst-italic">${itemDetail.status}</span>
          </div>
          <div class="row mb-1 ">
            <span class="col-4">Hình thức:</span>
            <span class="col-8 fst-italic">${itemDetail.order_type}</span>
          </div>
          <div class="row mb-1 ">
            <span class="col-4">Thực đơn:</span>
            <div class="col-8 fst-italic">
            ${itemDetail.order_items.map(item => 
              `<div class="row">
                <span class="col-8">${item.product.title} (x${item.amount}):</span>
                <span class="col-4">${item.amount * item.product.price} đ</span>
              </div>`
              ).join('')
            }
            </div>
          </div>
          <div class="row mb-1 ">
            <span class="col-4">Mã giảm giá:</span>
            <span class="col-8 fst-italic">${itemDetail.discount || '#'}</span>
          </div>
          <div class="row mb-1 ">
            <span class="col-4">Thành tiền:</span>
            <span class="col-8 fst-italic fw-bold">${itemDetail.total} đ</span>
          </div>
          <p class="fst-italic text-center">***********************************</p>
          <p class="fst-italic text-center fs-6 mb-0">Vui lòng đến thanh toán tại quầy để hoàn tất đơn hàng.</p>
          <div class="form-group mt-2">
            <div class="row">
              <div class="col-6 m-auto">
                <button onclick="confirmCancelOrder()" class="btn btn-outline-primary btn-block">Hủy đơn</button>
              </div>
              <div class="col-6 m-auto">
                <button onclick="requestPayment(${id})" class="btn btn-outline-primary btn-block">Thanh toán</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
  $('#order_detail_popup').html(stringHtml)
}

const renderListOrder = async () => {
  const response = await fetch (`/order-api/orders?store_operate=${store}`);
  const items = await response.json();
  orderList = items.results;
  const stringHtml =
  orderList.map(it =>
      `<div class="orders-item row g-0" onclick="popupOrderDetail(${it.id})">
        <div class="col-3 fw-bold text-primary">${it.id}</div>
        <div class="col-3">${it.order_type}</div>
        <div class="col-3">${it.total}</div>
        <div class="col-3"><span class="badge rounded-pill bg-warning text-dark">${it.status}</span></div>
      </div>`
    ).join('')
  $('.box-orders .orders-items').html(stringHtml);
}

const requestPayment = async (id) => {
  // const formData = new FormData();
  // formData.append('name', 'Thanh')
  // var dataPost = {
  //   async: true,
  //   crossDomain: true,
  //   processData: false,
  //   contentType: false,
  //   mimeType: "multipart/form-data",
  //   url: `/order-api/orders/request-payment/`,
  //   method: "POST",
  //   data: formData,
  // };
  // $.ajax(dataPost)
  //   .done(function (response) {
  //   console.log(response);
  //   });
  const response = await fetch (`/order-api/orders/${id}/request-payment/`);
  const data = await response.json();
  if (data.paymentUrl) {
    window.location.assign(data.paymentUrl)
  }
}

$(() => {
  renderListOrder();
})