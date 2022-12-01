var canvas = document.getElementById('myCanvas');
var ctx = canvas.getContext('2d');

var app = document.getElementById('app');
canvas.width = 250;
canvas.height = 150;

var mouse = {x: 0, y: 0};


var digit, accuracy,pr
    digit = document.getElementById('digit');
    accuracy = document.getElementById('aksara');
    pr = document.getElementById('p');


canvas.addEventListener('pointermove', function(e) {
  mouse.x = e.pageX - this.offsetLeft;
  mouse.y = e.pageY - this.offsetTop;
}, false);

ctx.lineWidth = 10;
ctx.lineJoin = 'round';
ctx.lineCap = 'round';
ctx.fillStyle = '#FFFFFF';
ctx.fill();
ctx.strokeStyle = '#000000';
ctx.stroke();

canvas.addEventListener('pointerdown', function(e) {
  mouse.x = e.pageX - this.offsetLeft;
  mouse.y = e.pageY - this.offsetTop;
  ctx.beginPath();
  ctx.moveTo(mouse.x, mouse.y);
  canvas.addEventListener('pointermove', onPaint, false);
}, false);

canvas.addEventListener('pointerup', function() {
  canvas.removeEventListener('pointermove', onPaint, false);
}, false);

var onPaint = function() {
  ctx.lineTo(mouse.x, mouse.y);
  ctx.stroke();
};

function clearArea() {
              // Use the identity matrix while clearing the canvas
              ctx.setTransform(1, 0, 0, 1, 0, 0);
              ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
              $('#digit').html('');
              $('#accuracy').html('');
              $('#p').html('');
            }
function save_image() {
              const link = document.createElement('a');
              var image = canvas.toDataURL();
              console.log(image);
              // clearArea();
              $.ajax({
                type: "POST",
                url: "/predict",
                data: {
                  imageBase64: image
                },
                beforeSend: function() {
                  pr.innerHTML = "Memproses masukan Anda...";

                }
              }).done(function(result) {
                digit.innerHTML = result.character
                aksara.innerHTML = result.aksara + '%'
                pr.innerHTML = 'Hasil Prediksi'
               
              });
            }