document.addEventListener('DOMContentLoaded', function() {
  fetch('header.html')
    .then(response => response.text())
    .then(data => {
      document.getElementById('header-placeholder').innerHTML = data;
      
      $('#aboutUs').click(function() {
        window.location.href = 'index.html';
      });
      $('#members').click(function() {
        window.location.href = 'membres.html';
      });
      $('#join').click(function() {
        window.location.href = 'join.html';
      });
      $('#writeups').click(function() {
        window.location.href = 'writeups.html';
      });
      $('#projects').click(function() {
        window.location.href = 'projects.html';
      });
      $('#contact').click(function() {
        window.location.href = 'contact.html';
      });
      
      const navToggle = document.querySelector('.nav-toggle');
      const navContainer = document.querySelector('.nav-container');
      
      navToggle.addEventListener('click', function() {
        navContainer.classList.toggle('active');
      });
    })
    .catch(error => console.error('Error loading header:', error));
  
  fetch('footer.html')
    .then(response => response.text())
    .then(data => {
      document.getElementById('footer-placeholder').innerHTML = data;
    })
    .catch(error => console.error('Error loading footer:', error));
});

