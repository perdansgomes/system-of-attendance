var images = document.querySelectorAll('.slider img');
var currentImageIndex = 0;
var intervalTime = 6000;
var preloadInterval = 0; 
  
function changeImage() {
  images[currentImageIndex].classList.remove('active');
  currentImageIndex = (currentImageIndex + 1) % images.length;
  images[currentImageIndex].classList.add('active');
}
  
function preloadImages() {
  images.forEach(function(image) {
    var img = new Image();
    img.src = image.src;
  });
}

function alerta(){
  var text = document.getElementById('result').value;
  var type_alert = document.getElementById('alert').value;
  var icon = '';
  var title = '';
  if(type_alert == 'True'){
    icon = 'success';
    title = 'Sucesso!';
  }
  if(type_alert == 'False'){
    icon = 'error';
    title = 'Oops...';
  }
  if(text != ""){
    document.getElementById('result').value = "";
    document.getElementById('alert').value = "";
    Swal.fire({
      icon: icon,
      title: title,
      text: text
    });
  }
}
  
function atrasaAlerta(){
  setTimeout(function(){alerta();},200);
}
  
window.onload = function() {
  preloadImages();
  setTimeout(function() {
    changeImage();
    setInterval(changeImage, intervalTime);
  }, preloadInterval);
  atrasaAlerta();
}