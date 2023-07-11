let allProduct = [];
let payMethod = 'cash';
$(document).ready( async function () {
  await getAllProduct();
  renderCart();
})

const handlePlaceOrder = () => {
  if (cartLS.length) {
    if(userLS?.phone) {
      $('#order_popup #logged_phone input').val(userLS.phone)
    } else {
      $('#order_popup #logged_phone').hide();
    }
    $('#order_popup').modal({
      open: true,
      fadeDuration: 200,
      showClose: false,
      escapeClose: true,
      clickClose: true,
    })
  }
}

const handlePay = (isAuth=null) => {
  if (!isAuth) {
    popupLogin()  
  } else {
    // call api create order and payment
    let formData = new FormData()
    formData.append('store_operate',store)
    formData.append('order_type','onsite')
    formData.append('items', JSON.stringify(cartLS))
    const crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
    const dataPost = {
      async: true,
      crossDomain: true,
      processData: false,
      contentType: false,
      headers: { "X-CSRFToken": crf_token },
      mimeType: "multipart/form-data",
      url: `/order-api/create-order/`,
      method: "POST",
      data: formData,
    };
    $("#processing").show();

    $.ajax(dataPost).done(function (response) {
      cartLS = [];
      localStorage.setItem('cart', JSON.stringify([]));
      $("#processing").hide();
      popupOrderSuccess(JSON.parse(response));
    }).fail(function (e) {
     $.notify("Có lỗi xảy ra, vui lòng thử lại.",
        {
          className: 'error',
          position: "top",
          autoHideDelay: 2000
        });
    });

    // const orderResult = {method: 'cash', orderHash: 'TSLKBPO4657SDF'}
  }
}
const getAllProduct = async () => {
  $('#processing').show();
  const response = await fetch (`/order-api/products`);
  const data = await response.json();
  allProduct = data?.results || [];
  $('#processing').hide();
}
const removeCart = (id) => {
  const newCart = cartLS.filter(item => +item.id !== +id);
  cartLS = [...newCart];
  localStorage.setItem('cart', JSON.stringify(newCart));
  renderCart();
};

const editCart = (cartId) => {
  window.location.assign(`/order-app/detail?store=${store}&cart=${cartId}`)
}

const renderCart = () => {
  const cartItems = cartLS.map(it => ({ ...allProduct.find(prd => prd.id === it.id), quantity: it.quantity, note: it.note }))
  const stringHtml =
    `<div class="items">
      ${ !cartItems?.length ? '<p class="no-item">No products available</p>' : cartItems.map(it =>
        ` <div class="cart-item">
            <div class="thumbnail">
              <img src="${it.thumbnail}" alt="">
            </div>
            <div class="info">
              <div class="title">${it.title}</div>
              <div class="note">Note: ${it.note}</div>
              <div class="quantity">Quantity: ${it.quantity}</div>
              <div class="total">Total: ${+it.price * it.quantity}$</div>
            </div>
            <div class="action">
              <button class="edit" onclick="editCart('${it.id}')">
                <img src="../static/order-app/images/your-cart/edit.png" alt="">
              </button>
              <button class="cancel" onclick="removeCart('${it.id}')">
                <img src="../static/order-app/images/your-cart/x.png" alt="">
              </button>
            </div>
          </div>
        `
      ).join('')}
    </div>` +
    `<div class="add-some-more">
    <a href=${APP_MENU_URLS.MENU}>
      <span>Add some more</span>
      <span class="icon-add">+</span>
    </a>
  </div>
  <div class="total-cart">
    <span>Total:</span>
    <span>${cartItems.map(c => +c.price * c.quantity).reduce((a, b) => a + b, 0)}$</span>
  </div>`
  $('.cart-items').html(stringHtml);
}
const selectPayMethod = (method) => {
  payMethod = method;
  $('.pay-method').removeClass('selected')
  $(`.${method}`).addClass('selected')
}