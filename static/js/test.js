
var swiper = new Swiper('.swiper-container', {
  scrollbar: {
      el: '.swiper-scrollbar',
  },
  pagination: {
      el: '.swiper-pagination',
      clickable: true,
      renderBullet: function (index, className) {
          return '<span class="' + className + '">' + (index + 1) + '</span>';
      },
  },
  // 缩略图配置
  thumbs: {
      swiper: {
          el: '.swiper-container-thumbnails',
          slidesPerView: 5,
          spaceBetween: 10,
          breakpoints: {
              640: {
                  slidesPerView: 3,
              },
              768: {
                  slidesPerView: 4,
              },
              1024: {
                  slidesPerView: 5,
              },
          },
      },
  },
});

// 缩略图和滚动条联动
swiper.controller.thumbs.swiper = swiper;
swiper.controller.control = swiper.thumbs.swiper;



const thumbnails = document.querySelector('.swiper-container-thumbnails');
const mainswiper = document.querySelector('.swiper-container');
// const header = document.querySelector('header');
// const wrapper = document.querySelector('#wrapper');

mainswiper.addEventListener('click', function() {
  if (thumbnails.style.display === 'none') {
    thumbnails.style.display = 'block';
  } else {
    thumbnails.style.display = 'none';
  }
});


