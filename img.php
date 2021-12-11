<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <title>Image Gallery</title>
  
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">

</head>

<body>

  <div class="container-fluid">
  <h3 class="text-center mt-3">Uploaded Images</h3>
  <h5 class="text-center">Gallery</h5>
    <?php
      $files = scandir('./images');
      echo "<div class='row'>";
      foreach ($files as $file) {
        if ($file !== "." && $file !== "..") {
          echo "<div class=' col-6 col-sm-4 col-md-3 mt-3 mb-3'>
                <img src='http://0.0.0.0:8000/$file' alt='image' width='100%' /></div>";
        }
      }
      echo "</div>";
    ?>
  </div>

</body>
</html>