function toggleTheme() {
    const body = document.body;
    const switchContainer = document.querySelector('.switch-container');
    body.classList.toggle('dark-mode');
    switchContainer.classList.toggle('dark');

    if (body.classList.contains('dark-mode')) {
      body.style.background = '#1e1e1e';
      body.style.color = '#ffffff';
    } else {
      body.style.background = '#e0e5ec';
      body.style.color = '#2d3436';
    }
  }