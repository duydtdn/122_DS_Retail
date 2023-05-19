$(document).ready(function () {
  renderCategories();
  renderPopularFood();
  renderPopularDrink();
  getDiscountPackage();
})
const getDiscountPackage = async () => {
  const response = await fetch (`/order-app/api/discount-packages`);
  const data = await response.json();
  renderListNews(data?.results)
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