let allProduct = [];
$(document).ready( async function () {
  await getAllProduct();
  renderCart();
  $('#btn_place_order').click(function () {
    cartLS = [];
    localStorage.setItem('cart', JSON.stringify([]));

    $('#place_order_popup').modal({
      open: true,
      fadeDuration: 200,
      showClose: false,
      escapeClose: false,
      clickClose: false,
    })
  })
})
const getAllProduct = async () => {
  const response = await fetch (`/order-app/api/orders/order-tables?tableId=4`);
  const data = await response.json();
  allProduct = data?.results || [];
}
const removeCart = (id) => {
  const newCart = cartLS.filter(item => +item.id !== +id);
  cartLS = [...newCart];
  localStorage.setItem('cart', JSON.stringify(newCart));
  renderCart();
};

const editCart = (cartId) => {
  window.location.assign(`/order-app/detail?cart=${cartId}`)
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
  <div class="end-line"></div>
  <div class="total-cart">
    <span>Total:</span>
    <span>${cartItems.map(c => +c.price * c.quantity).reduce((a, b) => a + b, 0)}$</span>
  </div>`
  $('.cart-items').html(stringHtml);
}