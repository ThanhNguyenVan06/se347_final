const menuIcon = document.getElementById('menuIcon');
const menu = document.getElementById('menu');
const wpUserLogged = document.getElementsByClassName('wp-user-logged')[0];
const userMenu = document.getElementsByClassName('user-menu')[0];
menuIcon.addEventListener('click', function(){
    menu.classList.toggle('active')
})
wpUserLogged.addEventListener('click', function(){
    userMenu.classList.toggle('active')
})