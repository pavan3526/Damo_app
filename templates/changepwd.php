<!DOCTYPE html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>Damo Dashboard</title>
  <!-- <link rel="stylesheet" href="css/style.css"> -->
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
  <!-- endinject -->
  <link rel="shortcut icon" href="images/favicon.png" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>




 <style type="text/css">
  .logo1{
    width : 200px;
    height : 60px;
  }
  .table_head{
    height: 70px;
  }
/*   .usertype{
    color: #337ab7;
    padding-right: 10px;
    position: relative;
    Bottom: 2px;
    font-size: 16px;
  }*/
 </style>
</head>
<body onload="Pageload()">
  <div class="container-scroller">
    <nav class="navbar col-lg-12 col-12 p-0 fixed-top d-flex flex-row">
      <div class="text-center navbar-brand-wrapper d-flex align-items-center justify-content-center">
        <img src="{{url_for('static', filename='logo.png')}}" class='image' align="middle">
      </div>
     <div class="navbar-menu-wrapper d-flex align-items-center justify-content-end">
           <div class="topnav changepassnav">
                        <a  href="/Scraper">Scraper</a>
                        <a href="/View">View / Edit data</a>
                        <a class="actived" href="/ChangePassword">Change Password</a>
                        <a href="/users_page" class='users'>Users</a>
                        <a href="/Production_tab?pgno=0" class='production'>Production</a>
                        <a href="/Notification_tab?pgno=0" class='Notification'>Notifications</a>
                        <a href="/keywords?valid=nofile" class='Keywords'>Keywords</a>
                        <a href="/downloadstab" class='Downloads'>Downloads</a>
                      </div>
        <div class = "row">
              <p class="usertype"> {{variable.usertype}} </p>
              <a type="submit" onclick="logout()" data-toggle="tooltip" title= {{variable.username}} ><i class="fa fa-power-off logout"  aria-hidden="true"></i></a>
        </div>
      </div>
    </nav>
    <!-- partial -->
        <div class="container-fluid page-body-wrapper">
      <!-- partial:partials/_sidebar.html -->
 <!--      <nav class="sidebar sidebar-offcanvas" id="sidebar">
        <ul class="nav">
          <li class="nav-item">
            <a class="nav-link" href="/Scraper">
              <i class="ti-shield menu-icon"></i>
              <span class="menu-title">Scraper</span>
            </a>
          </form>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/View">
              <i class="ti-layout-list-post menu-icon"></i>
              <span class="menu-title">View / edit data</span>
            </a>
          </li>
           <li class="nav-item">
            <a class="nav-link" href="/ChangePassword">
              <i class="ti-layout-list-post menu-icon"></i>
              <span class="menu-title">Change Password</span>
            </a>
          </li>
                   <li class="nav-item" id='users'>
            <a class="nav-link" href="/users_page">
              <i class="ti-layout-list-post menu-icon"></i>
              <span class="menu-title">Users</span>
            </a>
          </li>
        </ul>
      </nav> -->
      <!-- partial -->
      <div class="main-panel">
        <div class="content-wrapper">
          <div class="row">
            <div class="col-lg-12 grid-margin stretch-card">
              <div class="card">
                <div class="card-body">
                  <div class="msg">{{ variable.msg }}</div>
                   <div class="form-group">
                    <form action="/forgot_pwd" method="POST">
                      <div class="form-group">
                  <label for="Old_Password" class="webch">Old Password</label>
                  <input type="text"  class="form-control" style="width:300px;" id="Old_Password" name = 'Old_Password'>
                </div>
                      <div class="form-group">
                  <label for="New_Password" class="webch">New Password</label>
                  <input type="text" class="form-control" style="width:300px;" id="New_Password" name ='New_Password'>
                </div>
                      <div class="form-group">
                  <label for="Confirm_Password" class="webch">Confirm Password</label>
                  <input type="text"  class="form-control" style="width:300px;" id="Confirm_Password"  name = 'Confirm_Password'>
                </div>
                <button type="submit" id="submit1" class="btn btn-primary">Change Password</button>
              </form>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
             
<script type="text/javascript">
  function logout(){
    var r = confirm(" {{variable.username}} , Are you sure you want to logout")
    if(r == true){
      window.location.replace('/logout')
      console.log('true');
    }
    else{
      window.location.replace('/ChangePassword')
    }
  }
</script>
<script type="text/javascript">
function Pageload() {
  // if('{{variable.usertype}}' == 'Approver'){
  //   $('#Scraper').hide();
  // }
  if('{{variable.usertype}}' != 'Superadmin' && '{{variable.usertype}}' != 'Admin' ){
    $('.users').hide();
  }
  if('{{variable.usertype}}' != 'Superadmin'  && '{{variable.usertype}}' != 'Approver' ){
    $('.production').hide();
    $('.Notification').hide();
    $('.Keywords').hide();
  }
}
</script>
</body>

</html>
