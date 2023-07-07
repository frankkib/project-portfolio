function toggleForm() {
    var form = document.getElementById("house-form");
    form.style.display = form.style.display === "none" ? "block" : "none";
  }
  
  function previewImage(event) {
    var file = event.target.files[0];
    var reader = new FileReader();
    var imgElement = document.getElementById("preview");
  
    reader.onload = function(event) {
      imgElement.src = event.target.result;
    };
  
    reader.readAsDataURL(file);
  }
  
  function resizeImage() {
    var imgElement = document.getElementById("preview");
    var width = document.getElementById("width").value;
    var height = document.getElementById("height").value;
  
    imgElement.style.width = width + "px";
    imgElement.style.height = height + "px";
  }
  