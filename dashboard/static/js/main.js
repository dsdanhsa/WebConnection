const dropdown = document.querySelector('.side_bar-content.dropdown-btn');
const subMenu = document.querySelector('.submenu');

dropdown.onclick = function(){
    subMenu.classList.toggle('active');
}


const dropdown1 = document.querySelector('.side_bar-content.dropdown-btn1');
const subMenu1 = document.querySelector('.submenu1');

dropdown1.onclick = function(){
    subMenu1.classList.toggle('active1');
}