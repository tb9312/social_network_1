//upload to Cloudinary
document.getElementById("image").addEventListener("change", function (event) {
  var file = event.target.files[0];
  if (file) {
    var formData = new FormData();
    formData.append("file", file);
    formData.append("upload_preset", "gt9zxmci");

    // Send the image to Cloudinary
    fetch("https://api.cloudinary.com/v1_1/dtq4d7luc/image/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        // Update the image input field with the URL of the uploaded image
        document.getElementById("image_url").value = data.secure_url;
        var x = document.getElementById("image_url").value;
        console.log(x);
      })
      .catch((error) => {
        console.error("Error uploading image:", error);
      });
  }
});

//display image
document.getElementById("image").addEventListener("change", function (event) {
  var file = event.target.files[0];
  if (file) {
    var reader = new FileReader();
    reader.onload = function (e) {
      var previewImage = document.getElementById("previewImage");
      previewImage.src = e.target.result;
      previewImage.style.display = "block";
    };
    reader.readAsDataURL(file);
  }
});
