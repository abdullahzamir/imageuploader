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
  <h5 class="text-left mt-3">
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
    <div class="navbar-nav">
      <a class="nav-item nav-link" href="http://localhost:5000/index">Home</a>
      <a class="nav-item nav-link" href="http://localhost:5000/search">Search</a>
      <a class="nav-item nav-link" href="http://localhost:5000/delete">Delete</a>
    </div>
  </div>
</nav>
      </h1>
  <h3 class="text-center mt-3">Search results</h3>
  <h5 class="text-center">Gallery</h5>
    <?php
      $array_string = $argv[1];
      echo "<div class='row'>";
      $array = explode(' ', $array_string);
      foreach($array as $file) {
            echo "<div class=' col-6 col-sm-4 col-md-3 mt-3 mb-3'>
            <img src='http://localhost:8000/$argv[2]/$file' alt='image' width='100%' /></div>";
          
      }
      echo "</div>";
    ?>
  </div>

</body>
</html>