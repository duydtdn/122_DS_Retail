const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const id = +urlParams.get('id');
const cart = +urlParams.get('cart');
const store = +urlParams.get('store');
const path = window.location.pathname;
const API_URL = '/';
const APP_ROOT_URL = '/order-app/'
const APP_MENU_URLS = {
  HOME: `/order-app/home?store=${store}`,
  MENU: `/order-app/menu?store=${store}`,
  SIGNAGE: `/order-app/signage?store=${store}`,
  DETAIL: `/order-app/detail?store=${store}`,
  CART: `/order-app/cart?store=${store}`,
  PLACE_ORDERS: `/order-app/place-orders?store=${store}`,
}
const userLS = JSON.parse(localStorage.getItem('user'));
const accessToken = localStorage.getItem('access_token')

const onBack = () => history.back();
let cartLS = JSON.parse(localStorage.getItem('cart') || '[]');
let searchText = '';
let categoryFilter = '';
let groupText = '';
let categories = [];

const renderAppMenu = () => {
  const stringHtml = `
  <div class="wrapper">
    <a href="${APP_MENU_URLS.HOME}" class="menu-item ${APP_MENU_URLS.HOME.includes(path) ? 'active' : ''}">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="" xmlns="http://www.w3.org/2000/svg">
    <path d="M12.459 1.6605C12.3259 1.55674 12.162 1.5004 11.9932 1.5004C11.8245 1.5004 11.6606 1.55674 11.5275 1.6605L0.75 10.0642L1.68225 11.2433L3 10.2158V19.5C3.00079 19.8976 3.15908 20.2787 3.44022 20.5598C3.72135 20.8409 4.10242 20.9992 4.5 21H19.5C19.8976 20.9992 20.2787 20.8409 20.5598 20.5598C20.8409 20.2787 20.9992 19.8976 21 19.5V10.2225L22.3177 11.25L23.25 10.071L12.459 1.6605ZM13.5 19.5H10.5V13.5H13.5V19.5ZM15 19.5V13.5C14.9996 13.1023 14.8414 12.721 14.5602 12.4398C14.279 12.1586 13.8977 12.0004 13.5 12H10.5C10.1023 12.0004 9.721 12.1586 9.43978 12.4398C9.15856 12.721 9.0004 13.1023 9 13.5V19.5H4.5V9.0465L12 3.204L19.5 9.054V19.5H15Z" fill=""/>
    </svg>
    
      <div class="title">Home</div>
    </a>
    <a href="${APP_MENU_URLS.SIGNAGE}" class="menu-item ${APP_MENU_URLS.SIGNAGE.includes(path) && path !== APP_ROOT_URL ? 'active' : ''}">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="" xmlns="http://www.w3.org/2000/svg">
    <path d="M21 16H3V4H21M21 2H3C1.89 2 1 2.89 1 4V16C1 16.5304 1.21071 17.0391 1.58579 17.4142C1.96086 17.7893 2.46957 18 3 18H10V20H8V22H16V20H14V18H21C21.5304 18 22.0391 17.7893 22.4142 17.4142C22.7893 17.0391 23 16.5304 23 16V4C23 3.46957 22.7893 2.96086 22.4142 2.58579C22.0391 2.21071 21.5304 2 21 2Z" fill=""/>
    </svg>
    
      <div class="title">Signage</div>
    </a>
    <a href="${APP_MENU_URLS.MENU}" class="menu-item ${APP_MENU_URLS.MENU.includes(path) && path !== APP_ROOT_URL ? 'active' : ''}">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="" xmlns="http://www.w3.org/2000/svg">
    <path d="M4 6H20M4 12H20M4 18H20" stroke="" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>

      <div class="title">Menu</div>
    </a>
    <a href="${APP_MENU_URLS.PLACE_ORDERS}" class="menu-item ${APP_MENU_URLS.PLACE_ORDERS.includes(path) && path !== APP_ROOT_URL ? 'active' : ''}">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="" xmlns="http://www.w3.org/2000/svg">
    <g clip-path="url(#clip0_309_244)">
    <path d="M4.15625 4C3.58438 4 3.03593 4.22718 2.63155 4.63155C2.22718 5.03593 2 5.58438 2 6.15625V9.03125C2 9.60312 2.22718 10.1516 2.63155 10.5559C3.03593 10.9603 3.58438 11.1875 4.15625 11.1875H7.03125C7.60312 11.1875 8.15157 10.9603 8.55595 10.5559C8.96032 10.1516 9.1875 9.60312 9.1875 9.03125V6.15625C9.1875 5.58438 8.96032 5.03593 8.55595 4.63155C8.15157 4.22718 7.60312 4 7.03125 4H4.15625ZM12.7812 5.4375C12.5906 5.4375 12.4078 5.51323 12.273 5.64802C12.1382 5.78281 12.0625 5.96563 12.0625 6.15625C12.0625 6.34687 12.1382 6.52969 12.273 6.66448C12.4078 6.79927 12.5906 6.875 12.7812 6.875H24.2812C24.4719 6.875 24.6547 6.79927 24.7895 6.66448C24.9243 6.52969 25 6.34687 25 6.15625C25 5.96563 24.9243 5.78281 24.7895 5.64802C24.6547 5.51323 24.4719 5.4375 24.2812 5.4375H12.7812ZM12.7812 8.3125C12.5906 8.3125 12.4078 8.38823 12.273 8.52302C12.1382 8.65781 12.0625 8.84063 12.0625 9.03125C12.0625 9.22187 12.1382 9.40469 12.273 9.53948C12.4078 9.67427 12.5906 9.75 12.7812 9.75H21.4062C21.5969 9.75 21.7797 9.67427 21.9145 9.53948C22.0493 9.40469 22.125 9.22187 22.125 9.03125C22.125 8.84063 22.0493 8.65781 21.9145 8.52302C21.7797 8.38823 21.5969 8.3125 21.4062 8.3125H12.7812ZM4.15625 14.0625C3.58438 14.0625 3.03593 14.2897 2.63155 14.6941C2.22718 15.0984 2 15.6469 2 16.2188V19.0938C2 19.6656 2.22718 20.2141 2.63155 20.6185C3.03593 21.0228 3.58438 21.25 4.15625 21.25H7.03125C7.60312 21.25 8.15157 21.0228 8.55595 20.6185C8.96032 20.2141 9.1875 19.6656 9.1875 19.0938V16.2188C9.1875 15.6469 8.96032 15.0984 8.55595 14.6941C8.15157 14.2897 7.60312 14.0625 7.03125 14.0625H4.15625ZM12.7812 15.5C12.5906 15.5 12.4078 15.5757 12.273 15.7105C12.1382 15.8453 12.0625 16.0281 12.0625 16.2188C12.0625 16.4094 12.1382 16.5922 12.273 16.727C12.4078 16.8618 12.5906 16.9375 12.7812 16.9375H24.2812C24.4719 16.9375 24.6547 16.8618 24.7895 16.727C24.9243 16.5922 25 16.4094 25 16.2188C25 16.0281 24.9243 15.8453 24.7895 15.7105C24.6547 15.5757 24.4719 15.5 24.2812 15.5H12.7812ZM12.7812 18.375C12.5906 18.375 12.4078 18.4507 12.273 18.5855C12.1382 18.7203 12.0625 18.9031 12.0625 19.0938C12.0625 19.2844 12.1382 19.4672 12.273 19.602C12.4078 19.7368 12.5906 19.8125 12.7812 19.8125H21.4062C21.5969 19.8125 21.7797 19.7368 21.9145 19.602C22.0493 19.4672 22.125 19.2844 22.125 19.0938C22.125 18.9031 22.0493 18.7203 21.9145 18.5855C21.7797 18.4507 21.5969 18.375 21.4062 18.375H12.7812Z" fill=""/>
    </g>
    <defs>
    <clipPath id="clip0_309_244">
    <rect width="24" height="24" fill=""/>
    </clipPath>
    </defs>
    </svg>
          <div class="title">Orders</div>
    </a>
  </div>
      `;
  $('.app-menu-container .app-menu').html(stringHtml);
};
// const onChangeCategories = (key) => {
//   categoryFilter = key;
//   renderCategories(categoryFilter);
//   console.log({ searchText, groupText, categoryFilter })
//   if (path === APP_MENU_URLS.MENU) { return renderListOrderMenu(searchText, groupText, categoryFilter); }
//   if (path === APP_MENU_URLS.HOME || path === APP_ROOT_URL) {
//     renderPopularFood('', categoryFilter);
//     renderPopularDrink('', categoryFilter);
//   }
// }
const onSearch = () => {
  searchText = $('.search input').val();
  if (path === APP_MENU_URLS.MENU) { return renderListOrderMenu(searchText, groupText, categoryFilter); }
  if (path === APP_MENU_URLS.HOME || APP_ROOT_URL) {
    renderPopularFood(searchText, categoryFilter);
    renderPopularDrink(searchText, categoryFilter);
  }
}

// const renderCategories = async (activeKey) => {
//   if (!categories.length) {
//     const response = await fetch ('/order-api/categories');
//     const data = await response.json();
//     categories = data.results.filter(ct => ct.parent)
//   }
//   const stringHtml = `
//     <div class="title">Categories</div>
//       <div class="categories">
//         ${categories.map(ct =>
//     `<div onclick="onChangeCategories(${ct.id})" class="ctg-item ${ct.id === activeKey ? 'active' : ''}">${ct.name}</div>`).join('')}
//         </div>
//         </div>
//       `;
//   $('.section_categories').html(stringHtml);
// };
// const renderListOrderMenu = async (search = '', group = '', category = '') => {
//   const response = await fetch (`/order-api/products?category=${category}`);
//   const items = await response.json();
//   const stringHtml =
//     items.results.map(it =>
//       `<a class="order-item" href="${APP_MENU_URLS.DETAIL}?id=${it.id}"}>
//     <img class="thumbnail" src="${it.thumbnail}" alt="">
//     <span class="name">${it.title}</span>
//     <span class="price">${it.price} $</span>
//   </a>`
//     ).join('')
//   $('.section_items_order').html(stringHtml);
// }
const renderPopularFood = async (search = '', category = '') => {
  const response = await fetch (`/order-api/products?category=${category}`);
  const foods = await response.json();
  const stringHtml =
    foods.results.slice(0,2).map(it =>
      `<a class="order-item food" href="${APP_MENU_URLS.DETAIL}?id=${it.id}">
      <img class="thumbnail" src="${it.thumbnail}" alt="">
      <span class="name">${it.title}</span>
      <span class="price">${it.price} $</span>
    </a>`
    ).join('')
  $('.foods').html(stringHtml);
}
const renderPopularDrink = async (search = '', category = '') => {
  const response = await fetch (`/order-api/products?category=${category}`);
  const drinks = await response.json();
  const stringHtml =
  drinks.results.slice(0,2).map(it =>
    `<a class="order-item food" href="${APP_MENU_URLS.DETAIL}?id=${it.id}">
    <img class="thumbnail" src="${it.thumbnail}" alt="">
    <span class="name">${it.title}</span>
    <span class="price">${it.price} $</span>
  </a>`
    ).join('')
  $('.drinks').html(stringHtml);
}
const renderOrderCount = () => {
  $('.nav-box #order_count').html(cartLS.length || '')
}

const popupAccount = (username = '') => {
  $('#account_popup #account_username').val(username)
  $('#account_popup').modal({
    open: true,
    fadeDuration: 200,
    showClose: false,
    escapeClose: true,
    clickClose: true,
  });
}
const popupLogin = (open = true) => {
  // clear old form value
  $('#login_popup input').val('')
  $('#login_popup .error-text').html('')
  $('#login_popup').modal({
    open: open,
    fadeDuration: 200,
    showClose: false,
    escapeClose: true,
    clickClose: true,
  });
}

const popupRegister = () => {
  $('#register_step_1').removeClass('d-none').addClass('d-flex');
  $('#register_step_2').removeClass('d-flex').addClass('d-none');

  // clear old form value
  $('#register_popup input').val('')
  $('#register_popup .error-text').html('')

  $('#register_popup').modal({
    open: true,
    fadeDuration: 200,
    showClose: false,
    escapeClose: true,
    clickClose: true,
  });
}
const callPaymentIpn = async () => {
  const response = await fetch (`/order-api/payment-ipn${queryString}`);
  const data = await response.json(); 
}

const popupOrderSuccess = (onlinePay=false, orderResult) => {
  // if (onlinePay) {
  //   callPaymentIpn();
  // }
  $('#place_order_popup .order-hash.order-id').html(onlinePay ? orderResult : orderResult.data.id);
  $('.order-title').html(onlinePay ? 'Đặt hàng và thanh toán thành công!' : 'Đặt hàng thành công!')
  $('.notice').html(onlinePay ? 'Đơn hàng đang được xử lý, xin vui lòng đợi' : 'Vui lòng đến thanh toán tại quầy để hoàn tất đơn hàng')
  $('#place_order_popup').modal({
    open: true,
    fadeDuration: 200,
    showClose: false,
    escapeClose: false,
    clickClose: false,
  })
}
const handleLogin =  async () => {
  $('#login_popup #login_username_error').html('')
  $('#login_popup #login_password_error').html('')
  const username = $('#username').val();
  const password = $('#password').val();
  const user = {username, password}
  // const isValidPhone =validatePhoneNumber(+phone);
  const isValidUsername =validateUsername(username);
  const isValidPassword =validatePassword(password);
  if(isValidUsername && isValidPassword) {
    //call api login
    let formData = new FormData()
    formData.append('username',username)
    formData.append('password',password)
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
    const dataPost = {
      async: true,
      crossDomain: true,
      processData: false,
      contentType: false,
      mimeType: "multipart/form-data",
      url: `/order-api/auth/custom-login/`,
      method: "POST",
      data: formData,
    };
    $.ajax(dataPost).done(function (response) {
      window.location.reload();

    }).fail(function (e) {
      $('#login_popup #login_error').html('Sai tên đăng nhập hoặc mật khẩu.')
    });
   
  } else {
    $('#login_popup #login_username_error').html(isValidUsername ? '' : 'Tài khoản không hợp lệ')
    $('#login_popup #login_password_error').html(isValidPassword ? '' : 'Mật khẩu tối thiểu 6 ký tự không chứa ký tự đặc biệt')
  }
}
const handleRegister = () => {
  $('#register_popup #register_username_error').html('')
  $('#register_popup #register_password_error').html('')
  const username = $('#register_username').val();
  const password = $('#register_password').val();
  const user = {username, password}
  // const isValidPhone =validatePhoneNumber(+phone);
  const isValidUsername =validateUsername(username);
  const isValidPassword =validatePassword(password);
  if(isValidUsername && isValidPassword) {
    //send request register user
    let formData = new FormData()
    formData.append('username',username)
    formData.append('password',password)
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
    const dataPost = {
      async: true,
      crossDomain: true,
      processData: false,
      contentType: false,
      mimeType: "multipart/form-data",
      url: `/order-api/auth/custom-register/`,
      method: "POST",
      data: formData,
    };
    $("#processing").show();

    $.ajax(dataPost).done(function (response) {
        $.notify("Đăng ký tài khoản thành công, đăng nhập để tiếp tục...",
        {
          className: 'success',
          position: "top",
          autoHideDelay: 2000
        });
        setTimeout(() => {
          $("#processing").hide();
          popupLogin();
        }, 2000)

    }).fail(function (e) {
      $('#login_popup #login_error').html('Sai tên đăng nhập hoặc mật khẩu.')
    });
    //show confirm OTP popup
    // $('#register_step_1').addClass('d-none');
    // $('#register_step_2').removeClass('d-none').addClass('d-flex');
    // $('#digit1').focus();
  } else {
    $('#register_popup #register_username_error').html(isValidUsername ? '' : 'Tài khoản không hợp lệ')
    $('#register_popup #register_password_error').html(isValidPassword ? '' : 'Mật khẩu tối thiểu 6 ký tự không chứa ký tự đặc biệt')
  }
 
}
const confirmOtp = () => {
  const otp = $('#register_step_2 form').serializeArray().map(item => +item.value);
  if (otp.every((item) => item >= 0 && typeof item === 'number')) {
    //send request confirm otp

    //login to continue
    $("#processing").show();
    setTimeout(() => {
      // $('#register_popup').modal('toggle')
      $.notify("Đăng ký tài khoản thành công, chuyển đến đăng nhập...",
      {
        className: 'success',
        position: "top",
        autoHideDelay: 2000
      });
      setTimeout(() => {
        $("#processing").hide();
        popupLogin();
      }, 1000)
    }, 2000)
  }
}
// Show the spinner and overlay
function showSpinner() {
  $("#spinner").addClass("loading");
}

// Hide the spinner and overlay
function hideSpinner() {
  $("#spinner").removeClass("loading");
}
function validatePhoneNumber(phoneNumber) {
  // const regex = /^\d{9,11}$/;
  // return regex.test(phoneNumber);
  return true;
}
function validatePassword(password) {
  // const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$/;
  const regex = /^[a-zA-Z\d]{6,}$/;
  return regex.test(password);
}

function validateUsername(username) {
  const regex = /^[a-zA-Z\d]{6,}$/;
  return regex.test(username);
}

const handleLogout = () => {
  window.location.assign(`/order-app/logout?store=${store}`)
}
$(document).ready(function () {
  renderAppMenu();
  renderOrderCount();
  // auto focus next input when input OTP
  $('input[type="text"]').on('input', function() {
    var $this = $(this);
    if ($this.val().length == $this.attr('maxlength')) {
      $this.next().focus();
    }
  });
});
