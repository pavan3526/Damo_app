<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>HR Module</title>
  <link rel="stylesheet" href="css/style.css">
  <!-- endinject -->
  <link rel="shortcut icon" href="images/favicon.png" />
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">

   <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
 <style type="text/css">
 	.logo1{
 		width : 200px;
 		height : 60px;
 	}
 </style>
</head>
<body>
  <?php
  session_start();
  ?>
  <div class="container-scroller">
    <nav class="navbar col-lg-12 col-12 p-0 fixed-top d-flex flex-row">
      <div class="text-center navbar-brand-wrapper d-flex align-items-center justify-content-center">
        <img class ='logo1' src='logo.png'>
      </div>
      <div class="navbar-menu-wrapper d-flex align-items-center justify-content-end">
        <button class="navbar-toggler navbar-toggler align-self-center" type="button" data-toggle="minimize">
          <span class="ti-view-list"></span>
        </button>
              <a action = "/logout"><i class="fa fa-power-off" id="logout" aria-hidden="true"></i></a>
        </ul>
        <button class="navbar-toggler navbar-toggler-right d-lg-none align-self-center" type="button" data-toggle="offcanvas">
          <span class="ti-view-list"></span>
        </button>
      </div>
    </nav>
    <!-- partial -->
        <div class="container-fluid page-body-wrapper">
      <!-- partial:partials/_sidebar.html -->
      <nav class="sidebar sidebar-offcanvas" id="sidebar">
        <ul class="nav">
          <li class="nav-item">
            <a class="nav-link" href="Scraper.php">
              <i class="ti-shield menu-icon"></i>
              <span class="menu-title">Scraper</span>
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="View.php">
              <i class="ti-layout-list-post menu-icon"></i>
              <span class="menu-title">View / edit data</span>
            </a>
          </li>
           <li class="nav-item">
            <a class="nav-link" href="display.php">
              <i class="ti-layout-list-post menu-icon"></i>
              <span class="menu-title">Change Password</span>
            </a>
          </li>
        </ul>
      </nav>
      <!-- partial -->
      <div class="main-panel">
        <div class="content-wrapper">
          <div class="row">
            <div class="col-lg-12 grid-margin stretch-card">
              <div class="card">
                <div class="card-body">
                <div class="form-group">
                  <div class="row">
                  <label for="Website" class="web">Website Listing</label>
                  <input type="text" name = "Website" class="form-control" style="width:300px;" id="navbar-search-input" placeholder="Search Website.." aria-label="search" aria-describedby="search">
                </div>
                </div>
                  <div class="table-responsive">
                    <table class="table table-hover">
    <thead>
      <tr>
        <th>Website Name</th>
        <th>Type</th>
        <th>Latest date</th>
        <th>Last Refreshed on </th>
        <th>Requires Refresh</th>
        <th>Execute script</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>American Well</td>
        <td>Vendor</td>
        <td>03/Apr/2021</td>
        <td>03/Apr/2021</td>
        <td>Yes</td>
        <td><p  class="btn btn-primary btn-sm runbtn">Refresh</p></td>
        <!-- <td><p  class="btn btn-primary btn-sm runbtn">Download</p></td> -->
      </tr>
     <tr>
        <td>American Well</td>
        <td>Vendor</td>
        <td>03/Apr/2021</td>
        <td>03/Apr/2021</td>
        <td>Yes</td>
        <td><p  class="btn btn-primary btn-sm runbtn">Refresh</p></td>
      </tr>
      <tr>
        <td>American Well</td>
        <td>Vendor</td>
        <td>03/Apr/2021</td>
        <td>03/Apr/2021</td>
        <td>Yes</td>
        <td><p  class="btn btn-primary btn-sm runbtn">Refresh</p></td>
      </tr>
      <tr>
        <td>American Well</td>
        <td>Vendor</td>
        <td>03/Apr/2021</td>
        <td>03/Apr/2021</td>
        <td>Yes</td>
        <td><p  class="btn btn-primary btn-sm runbtn">Refresh</p></td>
      </tr>
      <tr>
        <td>American Well</td>
        <td>Vendor</td>
        <td>03/Apr/2021</td>
        <td>03/Apr/2021</td>
        <td>Yes</td>
        <td><p  class="btn btn-primary btn-sm runbtn">Refresh</p></td>
      </tr>
      <tr>
        <td>American Well</td>
        <td>Vendor</td>
        <td>03/Apr/2021</td>
        <td>03/Apr/2021</td>
        <td>Yes</td>
        <td><p  class="btn btn-primary btn-sm runbtn">Refresh</p></td>
      </tr>
      <tr>
        <td>American Well</td>
        <td>Vendor</td>
        <td>03/Apr/2021</td>
        <td>03/Apr/2021</td>
        <td>Yes</td>
        <td><p  class="btn btn-primary btn-sm runbtn">Refresh</p></td>
      </tr>
    </tbody>
  </table>
                </div>
              </div>
            </div>
      </div>
    </div>
  </div>
<!-- <script>
    $(document).on(function(){
        var form = $('#myform').serialize();
        $('#submit').click(function(){
        	console.log('Clicked');
            $.ajax({
                url: 'index.php',
                type: 'post',
                //data: 'hello',
                data: form,
                success: function(data){
                    console.log(data);
                }
            })
        })
    })
</script> -->
<!-- <script type="text/javascript">
  function logout(){
    if(confirm("<?php echo $_SESSION['uname'] ?> , Are you sure you want to logout")){
      window.location.replace("login.html");
    }
  }
</script> -->
</body>

</html>
