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

  <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-multiselect/0.9.13/js/bootstrap-multiselect.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-multiselect/0.9.13/css/bootstrap-multiselect.css">




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
                        <a href="/ChangePassword">Change Password</a>
                        <a href="/users_page" class='users'>Users</a>
                        <a href="/Production_tab?pgno=0" class='production'>Production</a>
                        <a href="/Notification_tab?pgno=0" class='Notification'>Notifications</a>
                        <a href="/keywords" class='Keywords'>Keywords</a>
                        <a class="actived" href="/downloadstab" class='Downloads'>Downloads</a>
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
                  <div class="table-responsive" style="padding-top:100px;">
                    <table class="table table-hover " id = 'websitelist'>
    <thead>
      <tr>
        <th>Id</th>
        <th>Website Name</th>
        <th>Status</th>
        <th>Created on</th>
        <th>Download</th>
      </tr>
    </thead>
    <tbody>
       {% for row in variable.data %}
            <tr class="content">
                <td >{{row[0]}}</td>
                <td >{{row[2]}}</td>
                <td >{{row[3]}}</td>
                <td >{{row[4]}}</td>
                <td><input class="btn btn-primary btn-sm runbtn accept" type="button" value="Download"></td>
            </tr>
        {% endfor %}
    </tbody>
  </table>
                </div>
                    <!-- <p style="font-size:17px;color:#8a8a8a;padding-top: 40px;">Refresh Keywords in already Scraped data</p>
                    <select multiple = 'multiple' id='Healthsystem' class="form-control">
                        <option disabled selected>Health System</option>
                        {% for row in variable.data %}
                        <option value= {{row[6]}} >{{row[6]}}</option> 
                        {% endfor %}
                      </select> &nbsp
                      <select multiple='multiple' id='filterText' class="form-control">
                        <option disabled selected>Approval Status</option>
                        <option value='Not Approved yet'>Not Approved yet</option>
                        <option value='Suggested Insertions'>Suggested Insertions</option>
                        <option value='Suggested Deletions'>Suggested Deletions</option>
                        <option value='Suggested Updates'>Suggested Updates</option>
                        <option value='Sent for Approval'>Sent for Approval</option>
                      </select>&nbsp
                      <br>
                      <button type="submit" id="oldrefresh" class="btn btn-primary runbtn">Keyword Map</button>
                      <button type="submit" id="accept" class="btn btn-primary runbtn">Download Accepted List </button>
                      <button type="submit" id="reject" class="btn btn-primary runbtn">Download  Rejected List </button> -->
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
      window.location.replace('/downloadstab')
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
  if('{{variable.usertype}}' != 'Superadmin' && '{{variable.usertype}}' != 'Admin' && '{{variable.usertype}}' != 'Approver' ){
    $('.production').hide();
    $('.Notification').hide();
    $('.Keywords').hide();
  }
  if('{{variable.filevalid}}' == 'validfile'){
    alert('Keywords got updated successfully !')
  }
  if('{{variable.filevalid}}' == 'invalidfile'){
    alert('Please check the file!!')
  }
  if('{{variable.typeofuploadkey}}' == 0){
    $('#newrefresh').hide();
  }
}
$(".Download_keywords").on('click', function() {
  console.log('click')
  window.location.replace('/Download_keywords')
});
$('#oldrefresh').on('click',function(){
  var value = $('#Healthsystem option:selected').text();
  console.log(value)
  var voyageId = new Array();
  $('#filterText option:selected').each(function () {
    voyageId.push($(this).val());
  });
  console.log(voyageId)
  $.ajax({
    url: '/Keywordmap',
    type:'POST',
    data : JSON.stringify({'data2':voyageId,'data1':value}),
    contentType: "application/json",
    success: function(response){
      console.log('No error')
    },
    error: function(error){
      console.log('U have done error')
      console.log(error);
    }
  });
});
// $('#accept').on('click',function(){
//   var value = $('#Healthsystem option:selected').text();
//   console.log(value)
//   window.location.replace('/Downloadaccepted?webname='+value)
// });
// $('#reject').on('click',function(){
//   var value = $('#Healthsystem option:selected').text();
//   console.log(value)
//   window.location.replace('/Downloadrejected?webname='+value)
// });

$('#filterText').multiselect();
$('#Healthsystem').multiselect();
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
    var len = $('table tr:not(.notfound) td:nth-child(2):contains("'+search+'")').length;

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

<!-- <script type="text/javascript">
  $(document).ready( function () {
    $('.refresh').on('click', function(){
      console.log('clicked')
      var currentRow = $(this).closest("tr");
      var tds = currentRow.find("td");
      var value = $(tds[1]).text();
      var condition = new Array();
      $('#filterText option:selected').each(function () {
        condition.push("'" +$(this).val()+ "'");
      });
      console.log(condition)
      $.ajax({
        url: '/Keywordmap',
        type:'POST',
        data : JSON.stringify({'data1': condition , 'data2':value}),
        contentType: "application/json",
        success: function(response){
          console.log(response['values']);
        },
        error: function(error){
          console.log('U have done error')
          console.log(error);
        }
      });
    });
  });
</script>
 -->
<script type="text/javascript">
  // $('#websitelist input[type=checkbox]').on('change', function (e) {
  //     if ($('#websitelist input[type=checkbox]:checked').length > 3) {
  //       $(this).prop('checked', false);
  //     }
  // });
  // $('.Multirefresh').on('click', function(){
  //   var weblist = []
  //   $("#websitelist input[type=checkbox]:checked").each(function () {
  //     var currentRow = $(this).closest("tr");
  //     var tds = currentRow.find("td");
  //     var value = $(tds[1]).text();
  //     weblist.push(value);
  //   });
  //   var condition = new Array();
  //   $('#filterText option:selected').each(function () {
  //       condition.push("'" +$(this).val()+ "'");
  //   });
  //   console.log(condition)
  //   console.log(weblist)
  //   $.ajax({
  //     url: '/Keywordmap',
  //     type:'POST',
  //     data : JSON.stringify({'data1': condition,'data2':weblist}),
  //     contentType: "application/json",
  //     success: function(response){
  //       console.log(response['values']);
  //     },
  //     error: function(error){
  //       console.log('U have done error')
  //       console.log(error);
  //     }
  //   });
  // });
</script>
<script type="text/javascript">
  $('.reset').on('click', function(){
    $.ajax({
      url: '/resetstatuskeywords',
      type:'POST',
      data : JSON.stringify({'data': 'reset'}),
      contentType: "application/json",
      success: function(response){
        console.log(response['status']);
        if(response['status'] == 0){
          alert('Cant reset the status')
        }
        else{
          alert('Reset done')
        }
      },
      error: function(error){
        console.log('U have done error')
        console.log(error);
      }
    });
  });
</script>

<script type="text/javascript">
  $(document).ready( function () {
    $('.accept').on('click', function(){
      console.log('clicked')
      var currentRow = $(this).closest("tr");
      var tds = currentRow.find("td");
      var value = $(tds[1]).text();
      var status = $(tds[2]).text();
      if (status == 'Download'){
        window.location.replace('/Down?webname='+value)
      }
      else{
        alert('Not yet Downloaded')
      }
    });
  });
</script>

</body>

</html>
