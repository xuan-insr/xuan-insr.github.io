<script>
function inFootnote(element) {
    let parent = element.parentNode;
    while (parent !== null) {
      if (parent.classList && parent.classList.contains("footnote")) {
        break;
      }
      parent = parent.parentNode;
    }
    return parent !== null;
}
</script>
<script>
function toggleVisibility() {
  const links = document.querySelectorAll('a');
  const buttons = document.querySelectorAll('.xyx-toggle');
  links.forEach(link => {
    if (!link.classList.contains('md-nav__link') &&
        !link.classList.contains('md-tabs__link') &&
        !link.classList.contains('md-source') &&
        !link.classList.contains('md-header__button') &&
        !link.closest('.md-nav__link') &&
        !link.closest('.md-tabs__link') &&
        !link.closest('.md-source') &&
        !link.closest('.footnote-backref') &&
        !link.closest('.footnote-ref') &&
        !link.closest('.md-header__button') &&
        !inFootnote(link)
        ) {
      if (link.style.display === 'none') {
        link.style.display = 'inline';
        for (const button of buttons) {
            button.innerHTML = '点击此处隐藏正文所有链接';
        }
      } else {
        link.style.display = 'none';
        for (const button of buttons) {
            button.innerHTML = '点击此处显示正文所有链接';
        }
      }
    }
  });
}
</script>
<script>
function toggleVisibilityFoot() {
  const links = document.querySelectorAll('a');
  const buttons = document.querySelectorAll('.xyx-toggle2');
  links.forEach(link => {
    if (link.closest('.footnote-backref') ||
        link.closest('.footnote-ref')) {
      if (link.style.display === 'none') {
        link.style.display = 'inline';
        for (const button of buttons) {
            button.innerHTML = '点击此处隐藏本文所有脚注';
        }
      } else {
        link.style.display = 'none';
        for (const button of buttons) {
            button.innerHTML = '点击此处显示本文所有脚注';
        }
      }
    }
  });

  const footnotes = document.querySelectorAll('.footnote');
  for (const footnote of footnotes) {
    if (footnote.style.display === 'none') {
      footnote.style.removeProperty('display');
    } else {
      footnote.style.display = 'none';
    }
  }
}
</script>

<center>
<button onclick="toggleVisibility()" class="box box-yellow xyx-toggle">点击此处隐藏正文所有链接</button>
<button onclick="toggleVisibilityFoot()" class="box box-green xyx-toggle2">点击此处隐藏本文所有脚注</button>
</center>