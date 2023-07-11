const headerToggleImg = document.querySelector('.header-toggle-img');
const breadcrumbs = document.querySelector('.breadcrumbs');
const header = document.querySelector('header');
const wrapper = document.querySelector('#wrapper');

headerToggleImg.addEventListener('click', function() {
  if (header.style.display === 'none') {
    header.style.display = 'block';
    wrapper.style.paddingTop = '70px';
    breadcrumbs.style.display = 'block';
  } else {
    header.style.display = 'none';
    breadcrumbs.style.display = 'none';
    wrapper.style.paddingTop = '0px';
  }
});