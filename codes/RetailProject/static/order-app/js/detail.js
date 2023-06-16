if (!id && !cart) {
  window.location.assign(APP_MENU_URLS.HOME)
}
const detailId = cart || id;

let product;
let price = 0;
let quantity = cart ? cartLS.find(it => it.id === detailId).quantity : 1;
let note = cart ? cartLS.find(it => it.id === detailId).note : '';
const increase = () => {
  quantity += 1;
  renderPrice(quantity)
}
const decrease = () => {
  quantity -= 1;
  if (quantity < 1) {
    quantity = 1;
  }
  renderPrice(quantity)
}
const renderPrice = (value) => {
  $('#quantity').text(value)
  $('#total').text(value * price + '$');
}
const getDetail = async () =>{
  const response = await fetch (`/order-app/api/products/${detailId}`);
  const data = await response.json();
  product = data;
  price = product.price
  renderDetail()
  renderPopupAddToCart();
}

$(document).ready(function () {
  getDetail();
  if (cart) {
    $("#add_to_cart_popup").modal({
      open: true,
      fadeDuration: 200,
      showClose: false,
      escapeClose: true,
      clickClose: true,
    });
    renderPrice(quantity)
  }
  $('#btn_add_to_cart').click(function () {
    $("#add_to_cart_popup").modal({
      open: true,
      fadeDuration: 200,
      showClose: false
    });
    renderPrice(quantity)
  });
})
const renderDetail = () => {
  const stringHtml =
    `<div class="thumbnail-top remove-margin">
      <img src="${product.thumbnail}" alt="">
    </div>
    <div class="section_detail">
      <div class="title">${product.title}</div>
      <div class="sub-title">${product.category.name}</div>
      <div class="desc">${product.detail}</div>
      <div class="price">Price:
        <span>${product.price}$</span>
      </div>
    </div>`
  $('#product-detail').html(stringHtml);
}
const renderPopupAddToCart = () => {
  const stringHtml =
    `<div class="title">${product.title}</div>
    <div class="sub-title">${product.category.name}</div>
    <div class="desc">${product.detail}</div>
    <div class="price">
      Price:
      <span>${product.price} $</span>
    </div>
    <div class="quantity">
      Quantity:
      <button onclick="decrease()">-</button>
      <span id="quantity">
        ${quantity}
      </span>
      <button onclick="increase()">+</button>
    </div>
    <div class="total">
      Total:&nbsp;
      <span id="total">${product.price} $</span>
    </div>
    <textarea placeholder="Note">${note}</textarea>`
  $('#add_to_cart_popup .section_detail').html(stringHtml);
}

const addToCart = () => {
  const noteText = $('.section_detail textarea').val() || '';
  if (!cart) {
    // Add new cart
    const index = cartLS.findIndex((item) => item.id === product.id);
    if (index < 0) {
      cartLS.push({ id: product.id, quantity: quantity, note: noteText });
    } else {
      cartLS[index] = { id: product.id, quantity: cartLS[index].quantity + quantity, note: noteText }
    }
  } else {
    // Edit cart
    cartLS = [
      ...cartLS.filter(c => c.id !== product.id),
      { id: product.id, quantity: quantity, note: noteText }
    ]
  }
  localStorage.setItem('cart', JSON.stringify(cartLS))
  $("#add_to_cart_popup").modal('toggle');
  $.notify("Add to cart successfully",
    {
      className: 'success',
      position: "top center",
      // showAnimation: 'slideDown',
      // hideAnimation: 'slideUp',
      autoHideDelay: 1000
    });
  setTimeout(() => {
    if (!cart) {
      window.location.assign(APP_MENU_URLS.HOME)
    } else {
      window.location.assign(APP_MENU_URLS.CART)
    }
  }, 1000);
}