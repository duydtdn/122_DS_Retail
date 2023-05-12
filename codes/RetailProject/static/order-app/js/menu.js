groupText = urlParams.get('group') || '';

$(document).ready(function () {
  renderCategories();
  renderListOrderMenu('', groupText, '');
})