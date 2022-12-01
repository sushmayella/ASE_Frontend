var hom = document.getElementById('home');
var password_page = document.getElementById('password_page');

var b1 = document.getElementById('b1');
var b5 = document.getElementById('b5');


function home(){
password_page.style.display='none';
hom.style.display='block';
b5.classList.add('bg-secondary');
b1.classList.remove('bg-secondary');
}

function password(){
password_page.style.display='block';
hom.style.display='none';
b5.classList.remove('bg-secondary');
b1.classList.add('bg-secondary');
}