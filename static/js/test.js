
var swiper = new Swiper('.swiper-container', {
    effect: 'fade', // 添加此行来设置淡入淡出效果
    fadeEffect: {
        crossFade: true, // 添加此行来实现淡入淡出效果的交叉渐变
    },   
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
          effect: 'fade', // 添加此行来设置淡入淡出效果
          fadeEffect: {
              crossFade: true, // 添加此行来实现淡入淡出效果的交叉渐变
          },   
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








