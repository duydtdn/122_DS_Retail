$(document).ready(function () {
  renderCategories();
  renderPopularFood();
  renderPopularDrink();
  getDiscountPackage();
  renderOrderStatus();
});

const getDiscountPackage = async () => {
  const response = await fetch (`/order-app/api/discount-packages`);
  const data = await response.json();
  renderListNews(data?.results)
}
const renderOrderStatus = async () =>  {
  const response = await fetch (`/order-app/api/tables?is_available=1`);
  const data = await response.json();
  const stringHtml = `
    <div class="text">
        <div>${data.results.length} Available</div>
        <div>Tables</div>
    </div>
  `
  $('.tables').html(stringHtml)
}

function renderListNews(data) {
  const stringHtml = [...data].map(it => `
  <div class="swiper-slide">
    <div class="discount-packages-item">
      <img src="${it.thumbnail}"/>
      <div class="content d-flex flex-column">
        <div class="title">${it.title}</div>
      </div>
    </div>
  </div>
  `).join("");
  $('.banner .discount-packages-swipper .swiper-wrapper').html(stringHtml);
  const swiper = new Swiper(".discount-packages-swipper", {
  pagination: {
    el: ".swiper-pagination",
  },
  slidesPerView: 1,
  spaceBetween: 20,
  autoplay: {
    delay: 3000,
  },
  loop:true
  });
}