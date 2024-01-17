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
<!--     <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
 -->

   <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>

 <style type="text/css">
  .logo1{
    width : 200px;
    height : 60px;
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
      <img src="{{url_for('static', filename='logo.png')}}" class='image'  align="middle">
      </div>
      <div class="navbar-menu-wrapper d-flex align-items-center justify-content-end">
           <div class="topnav viewnav">
                        <a href="/Scraper">Scraper</a>
                        <a class="actived" href="/View">View / Edit data</a>
                        <a href="/ChangePassword">Change Password</a>
                        <a href="/users_page" class='users'>Users</a>
                        <a href="Production_tab?pgno=1" class='production'>Production</a>
                        <a href="/Notification_tab?pgno=1" class='Notification'>Notifications</a>
                        <a href="/keywords?valid=nofile" class='Keywords'>Keywords</a>
                        <a href="/downloadstab" class='Downloads'>Downloads</a>
                      </div>
          <p class="usertype"> {{variable.usertype}} </p>
              <a type="submit" onclick="logout()" data-toggle="tooltip" title= {{variable.username}} ><i class="fa fa-power-off scraperpoweroff" aria-hidden="true"></i></a>
      </div>
    </nav>
    <!-- partial -->
        <div class="container-fluid page-body-wrapper">
      <!-- partial:partials/_sidebar.html -->
     <!--  <nav class="sidebar sidebar-offcanvas" id="sidebar">
        <ul class="nav">
        <li class="nav-item" id='Scraper'>
          <a class="nav-link" href="/Scraper">
          <i class="ti-shield menu-icon"></i>
          <span class="menu-title">Scraper</span>
        </a>
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
                   <div class="form-group">
                  <div class="row">
                  <label for="Website" class="web">Website Listing</label>
                  <input type="text" name = "Website" class="form-control" style="width:300px;" id="navbar-search-input" placeholder="Search Website.." aria-label="search" aria-describedby="search">
                </div>
                </div>
                  <div class="table-responsive">
                    <table class="table table-hover" id ="websitelist">
    <thead>
      <tr>
        <th>Website Name</th>
        <th>Type</th>
        <th>Last Refreshed on </th>
        <th>View data </th>
        <th>Download all</th>
        <th>Download accepted</th>
        <th>Download rejected</th>
      </tr>
    </thead>
      <tbody>
       {% for row in variable.data %}    
            <tr>
                <td >{{row[6]}}</td>
                <td>{{row[4]}}</td>
                <td>{{row[14]}}</td>
                <td><p class="btn btn-primary btn-sm runbtn View">View</p></td>
                <td><p class="btn btn-primary btn-sm runbtn Download">Download</p></td>
                <td><input class="btn btn-primary btn-sm runbtn accept" type="button" id="{{row[6]}}" value="Download Accepted"></td>
                <td><input class="btn btn-primary btn-sm runbtn reject" type="button" id="{{row[6]}}" value="Download Rejected"></td>
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
      window.location.replace('/View')
    }
  }
</script>
<!-- <script type="text/javascript">
  $("#navbar-search-input").on("keyup", function() {
    var value = $(this).val();
    $("table tr").each(function(index) {
        if (index !== 0) {

            $row = $(this);

            var id = $row.find("td:first").text();

            if (id.indexOf(value) !== 0) {
                $row.hide();
            }
            else {
                $row.show();
            }
        }
    });
});
</script> -->
<script type="text/javascript">
function Pageload() {
  $('#websitelist_filter').hide();
  $('#websitelist_length').hide();
  // if('{{variable.usertype}}' == 'Approver'){
  //   $('#Scraper').hide();
  // }
  if('{{variable.usertype}}' != 'Superadmin' && '{{variable.usertype}}' != 'Admin' )
  {
    $('.users').hide();
  }
  if('{{variable.usertype}}' != 'Superadmin'  && '{{variable.usertype}}' != 'Admin' && '{{variable.usertype}}' != 'Approver' )
  {
    $('.production').hide();
    $('.Notification').hide();
    $('.Keywords').hide();
  }
  if('{{variable.username}}' == ''){
    window.location.replace('/login')
  }

}
</script>
<!-- <script type="text/javascript">
  $(document).ready( function () {
    $('#websitelist').DataTable();
} );
</script> -->
<script type="text/javascript">
    $(".View").on('click', function() {
      console.log('clicked')
      var currentRow = $(this).closest("tr");
      var tds = currentRow.find("td");
      var value = $(tds[0]).text() ;
      const value1 = 0
      window.location.replace('/Display?id='+value+'&pgno='+value1)
    });
    $('.Download').on('click', function(){
      console.log('clicked')
      var currentRow = $(this).closest("tr");
      var tds = currentRow.find("td");
      var value = $(tds[0]).text();
      alert(value+ ' scheduled to download')
      $.ajax({
        url: '/Download_file',
        type:'POST',
        data : JSON.stringify({'data': value}),
        contentType: "application/json",
        success: function(response){
          console.log(response['websitename']);
          var web = response['websitename'];
        },
        error: function(error){
          console.log('U have done error')
          console.log(error);
        }
      });
    });
</script>
<script type="text/javascript">
  $(document).ready(function(){
  $('#navbar-search-input').keyup(function(){
    // Search Text
    console.log('entered')
    var search = $(this).val();

    // Hide all table tbody rows
    $('table tr').hide();

    // Count total search result
    var len = $('table tr:not(.notfound) td:nth-child(1):contains("'+search+'")').length;

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
$.expr[":"].contains = $.expr.createPseudo(function(arg) {
   return function( elem ) {
     return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
   };
});
</script>
<script type="text/javascript">
  $(document).ready( function () {
    $('.accept').on('click', function(){
      console.log('clicked')
      var currentRow = $(this).closest("tr");
      var tds = currentRow.find("td");
      var value = $(tds[0]).text();
      alert(value+ ' Accepted list scheduled to download')
      $.ajax({
        url: '/Downloadaccepted',
        type:'POST',
        data : JSON.stringify({'data': value}),
        contentType: "application/json",
        success: function(response){
          console.log(response['websitename']);
          var web = response['websitename'];
        },
        error: function(error){
          console.log('U have done error')
          console.log(error);
        }
      });
    });
    $('.reject').on('click', function(){
      console.log('clicked')
      var currentRow = $(this).closest("tr");
      var tds = currentRow.find("td");
      var value = $(tds[0]).text();
      alert(value+ ' Rejected list scheduled to download')
      $.ajax({
        url: '/Downloadrejected',
        type:'POST',
        data : JSON.stringify({'data': value}),
        contentType: "application/json",
        success: function(response){
          console.log(response['websitename']);
          var web = response['websitename'];
        },
        error: function(error){
          console.log('U have done error')
          console.log(error);
        }
      });
    });
  });
</script>

</body>

</html>
