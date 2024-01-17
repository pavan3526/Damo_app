<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
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
 /* .usertype{
    color: #337ab7;
    padding-right: 10px;
    position: relative;
    bottom: 2px;
    font-size: 16px;
  }*/
  #create_user{
    position: relative;
    left: 1020px;

  }
 </style>
</head>
<body onload="Pageload()">
  <?php
  session_start();
  ?>
  <div class="container-scroller">
    <nav class="navbar col-lg-12 col-12 p-0 fixed-top d-flex flex-row">
      <div class="text-center navbar-brand-wrapper d-flex align-items-center justify-content-center">
        <img src="{{url_for('static', filename='logo.png')}}" class='image' align="middle">
      </div>
     <div class="navbar-menu-wrapper d-flex align-items-center justify-content-end">
           <div class="topnav usersnav">
                        <a href="/Scraper">Scraper</a>
                        <a href="/View">View / Edit data</a>
                        <a href="/ChangePassword">Change Password</a>
                        <a class="actived" href="/users_page" class='users'>Users</a>
                        <a href="Production_tab?pgno=0" class='production'>Production</a>
                        <a href="/Notification_tab?pgno=1" class='Notification'>Notifications</a>
                        <a href="/keywords?valid=nofile" class='Keywords'>Keywords</a>
                        <a href="/downloadstab" class='Notification'>Downloads</a>
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
<!--       <nav class="sidebar sidebar-offcanvas" id="sidebar">
        <ul class="nav">
          <li class="nav-item" id = 'Scraper'>
            <a class="nav-link" href="/Scraper">
              <i class="ti-shield menu-icon"></i>
              <span class="menu-title">Scraper</span>
            </a>
          </form>
          </li>
          <li class="nav-item" id = 'Edit'>
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
          <li class="nav-item">
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
                  <button type="button" class="btn btn-primary btn-sm runbtn" id = 'create_user' data-toggle="modal" data-target="#myModal">Add User</button>
                <div class="form-group">
                  <div class="row">
                  <label for="Website" class="web">Users:</label>
                  <input type="text" name = "Website" class="form-control" style="width:300px;" id="navbar-search-input" placeholder="Search User.." aria-label="search" aria-describedby="search">


                </div>

<!--                 <button type="button" value="selectAll" class=" btn btn-primary btn-sm runbtn main" onclick="checkAll()">Select All</button>
                <button type="button" value="deselectAll" class="btn btn-primary btn-sm runbtn main" onclick="uncheckAll()">Clear</button>
                <td><p  class="btn btn-primary btn-sm runbtn">Delete</p></td> -->
                </div>
                

  <!-- Modal -->
  <div class="modal fade" id="myModal" role="dialog">
    <div class="modal-dialog">
    
      <!-- Modal content-->
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal">&times;</button>
        </div>
        <div class="modal-body">
          <form action="/user_insert" method="POST">
 <!--  <div class="form-group">
    <label for="uid">User ID:</label>
    <input type="text" class="form-control" name='uid' id="uid">
  </div> -->
    <div class="form-group">
    <label for="uname">Username:</label>
    <input type="text" class="form-control" name='uname' id="uname">
  </div>
  <div class="form-group">
    <label for="pwd">Password:</label>
    <input type="text" class="form-control" name='pwd' id="pwd">
  </div>
  <div class="form-group">
  <label for="sel1">Select Role:</label>
  <select class="form-control" name = 'role' id="role">
    <option value = 'Admin'>Admin</option>
    <option value = 'Analyst'>Analyst</option>
    <option value = 'Approver'>Approver</option>
  </select>
</div>
<button  id="submit1" class="btn btn-primary btn-sm runbtn">Create User</button>
</form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>
        </div>
      </div>
      
    </div>
  </div>
                  <div class="table-responsive">
                    <table class="table table-hover">
    <thead>
      <tr>
        <th>ID</th>
        <th>UserID</th>
        <th>Username</th>
        <th>Password</th>
        <th>Role</th>
        <th>Status</th>
        <th>Created on</th>
        <th>Created by </th>
        <th>Last Login </th>
        <th> Action </th>
      </tr>
    </thead>
    <tbody>
     {% for row in variable.data %}    
            <tr>
                <td>{{row[0]}}</td>
                <td>{{row[1]}}</td>
                <td>{{row[2]}}</td>
                <td>{{row[3]}}</td>
                <td>{{row[4]}}</td>
                <td>{{row[5]}}</td>
                <td>{{row[6]}}</td>
                <td>{{row[7]}}</td>
                <td>{{row[8]}}</td>
                <td><p  class="btn btn-primary btn-sm runbtn delete">Delete</p></td>
            </tr>
        {% endfor %}
    </tbody>
  </table>
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
      window.location.replace('/users_page')
    }
  }
</script>
<script type="text/javascript">
  $(document).ready(function() {
    $(".delete").on('click', function() {
      console.log('clicked')
      var currentRow = $(this).closest("tr");
      var tds = currentRow.find("td");
      console.log(tds[0]);
      var r = confirm("Are you sure you want to delete " + $(tds[2]).text())
      var value = $(tds[0]).text() ;
      if(r == true){
        $.ajax({
          url: '/delete_user',
          type:'POST',
          data : JSON.stringify({'data': value}),
          contentType: "application/json",
          
          success: function(response){
            window.location.replace('/users_page')
          },
          error: function(error){
            console.log('U have done error')
            console.log(error);
          }
        });
        // window.location.replace('/delete')
      }
      else{
        window.location.replace('/users_page')
      }
    });
  });
</script>
<script type="text/javascript">
function Pageload() {
  console.log('Approver');
  // if('{{variable.usertype}}' == 'Admin'){
  //   $('#Edit').hide();
  // }
  if('{{variable.usertype}}' != 'Superadmin' && '{{variable.usertype}}' != 'Admin' ){
    $('.users').hide();
  }
  if('{{variable.usertype}}' != 'Superadmin'  && '{{variable.usertype}}' != 'Approver' ){
    $('.production').hide();
    $('.Notification').hide();
  }
}
</script>
<!-- Using below code for live search -->
<script type="text/javascript">
  $(document).ready(function(){

  // Search all columns
  // $('#txt_searchall').keyup(function(){
  //   // Search Text
  //   var search = $(this).val();

  //   // Hide all table tbody rows
  //   $('table tbody tr').hide();

  //   // Count total search result
  //   var len = $('table tbody tr:not(.notfound) td:contains("'+search+'")').length;

  //   if(len > 0){
  //     // Searching text in columns and show match row
  //     $('table tbody tr:not(.notfound) td:contains("'+search+'")').each(function(){
  //       $(this).closest('tr').show();
  //     });
  //   }else{
  //     $('.notfound').show();
  //   }

  // });

  // Search on name column only
  $('#navbar-search-input').keyup(function(){
    // Search Text
    console.log('entered')
    var search = $(this).val();

    // Hide all table tbody rows
    $('table tr').hide();

    // Count total search result
    var len = $('table tr:not(.notfound) td:nth-child(3):contains("'+search+'")').length;

    if(len > 0){
      // Searching text in columns and show match row
      $('table tr:not(.notfound) td:contains("'+search+'")').each(function(){
         $(this).closest('tr').show();
      });
    }else{
      $('.notfound').show();
    }

  });

});

// Case-insensitive searching (Note - remove the below script for Case sensitive search )
$.expr[":"].contains = $.expr.createPseudo(function(arg) {
   return function( elem ) {
     return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
   };
});
</script>
</body>

</html>
