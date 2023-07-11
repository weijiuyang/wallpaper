// 获取分页元素
var pagination = document.querySelector('.pagination');

// 获取当前页元素
var currentPage = document.querySelector('span');
console.log(currentPage)
// 绑定点击事件
pagination.addEventListener('click', function(event) {
  // 取消默认行为
  event.preventDefault();

  // 获取当前页码
  var current = parseInt(currentPage.textContent);
  console.log(current)

  // 获取总页数
  var total = pagination.children.length - 2;

  // 获取点击的元素
  var target = event.target;

  // 根据点击的元素更新当前页码
  if (target.textContent === '«') {
    current = Math.max(current - 1, 1);
  } else if (target.textContent === '»') {
    current = Math.min(current + 1, total);
  } else {
    current = parseInt(target.textContent);
  }

  // 更新当前页码显示
  currentPage.textContent = '当前页：' + current;

  // 更新分页链接状态
  pagination.children[current].classList.add('active');
  for (var i = 1; i <= total; i++) {
    if (i !== current) {
      pagination.children[i].classList.remove('active');
    }
  }
});