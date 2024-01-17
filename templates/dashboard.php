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
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>



 <style type="text/css">
  .logo1{
    width : 200px;
    height : 60px;
  }
  .table_head{
    height: 40px;
  }
  .table_body{
  	height : 20px;
  }
  td {
    max-width: 100px !important;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .db2{
    padding: 10px;
  }
  tr {
   line-height: 25px;
   min-height: 25px;
   height: 25px;
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
           <div class="topnav adminnav">
                        <a href="/Scraper">Scraper</a>
                        <a class='actived' href="/View">View / Edit data</a>
                        <a href="/ChangePassword">Change Password</a>
                        <a href="/users_page" class='users'>Users</a>
                        <a href="/downloadstab" class='Notification'>Downloads</a>
                      </div>
        <div class = "row">
              <p class="usertype"> {{variable.usertype}} </p>
              <a type="submit" onclick="logout()" data-toggle="tooltip" title= {{variable.username}} ><i class="fa fa-power-off poweroff logout" aria-hidden="true"></i></a>
        </div>
      </div>
    </nav>
    <!-- partial -->
        <div class="container-fluid page-body-wrapper">
      <!-- partial:partials/_sidebar.html -->
<!--       <nav class="sidebar sidebar-offcanvas" id="sidebar">
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
              <div class="card db2">
                <div class="card-body">
                   <div class="form-group">
               <!--    <div class="row">
                  <label for="Website" class="web">Website: <?php  $website_name; ?></label>
                  <input type="text" name = "Website" class="form-control" style="width:300px;" id="navbar-search-input" placeholder="Search text.." aria-label="search" aria-describedby="search">
                </div> -->
                <div class ="row">
     <div class="dropdown">
<!--                           <button class="btn btn-info runbtn select1" type="button" id="dropdownmenu" data-toggle="dropdown" aria-haspopup="false" aria-expanded="false">Select by Name of the Organization</button>
                          <div class="dropdown-menu" aria-labelledby="dropdownmenu">
                            <h6 class="dropdown-header">Dropdown Header</h6>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="#">Dropdown One</a>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="#">Dropdown Two</a>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="#">Dropdown Three</a>
                          </div>
                          <button class="btn btn-info runbtn select2" type="button" id="dropdownmenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Select by Vendor</button>
                          <div class="dropdown-menu" aria-labelledby="dropdownmenu1">
                            <h6 class="dropdown-header">Dropdown Header</h6>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="#">Dropdown One</a>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="#">Dropdown Two</a>
                          </div> -->
                          <!-- <p class="btn btn-primary btn-sm runbtn approval">Approve</p>
                          <p  class="btn btn-primary btn-sm runbtn Production">Move to Production</p> -->
                           <div class = 'row'>
                          <p class="subhead"><b> Website Name : </b> {{variable.value}} </p>
                          <p class="subhead"><b> No of Articles : </b> {{variable.articlecount}} </p>

                          <div class='fourbtn'>
                         <!--  <p class="btn btn-primary btn-sm runbtn approval">Approve</p>
                          <p  class="btn btn-primary btn-sm runbtn Production">Move to Production</p> -->
                          <p  class="btn btn-primary btn-sm runbtn Downexcel">Download this Page</p>
                           <!-- <form enctype="multipart/form-data" method='POST' action='/fileupload1' id='upfile'>
                            <div class="uploadfile">
                              <input type="file" id='file' name='file' class='fileupload'/>
                              <button type='submit' class="btn btn-primary btn-sm runbtn Upexcel">Upload Excel</button>
                              <input type='text' value = '{{variable.value}}' name ='webname' style="display: none;">
                              <input type='text' value = '{{variable.pgid}}' name ='pgid' style="display: none;">
                            </div>
                          </form> -->
                        </div>
                        <p class="subhead"><b> No of pages : </b> {{variable.noofpages}} </p>
                  <form class="form-inline"  action="/arsearch" method="POST">
                    <div class="form-group">
                      <input class="form-control an_search" id="asearch" name='asearch' placeholder="Enter page Number" type="text">
                    </div>
                    <br>
                    <input type='text' value = '{{variable.value}}' name ='webname' style="display: none;">
                    <button type="submit"  name="submit" class="btn btn-primary btn-sm runbtn an_pg">Search</button>
                  </form>

                  <form class="form-inline" action="/singlearsearch" method="POST" style='padding-left:70px;'>
                    <div class="form-group">
                      <input class="form-control an_search" id="artsearch" name='artsearch' placeholder="Enter article Number" type="text">
                    </div>
                    <br>
                    <input type='text' value = '{{variable.value}}' id='websitename' name ='webname' style="display: none;">
                    <button  class="btn btn-primary runbtn an_pg btn-sm">Search</button>
                  </form>
                        </div>
                </div>
                  <div class="table-responsive">
                  	<table class="table table-hover table-bordered table-striped " id="table">
    <thead>
      <tr class="table_head">
        <th>Select</th>
        <th style="width: 5% ...">Article id</th>
        <th style="width: 5% ...">Date</th>
        <th style="width: 2% ...">Healthcare Enterprise</th>
        <th style="width: 5% ...">Technology Category </th>
        <th style="width: 5% ...">Use Case</th>
        <th style="width: 5% ...">Vendor</th>
        <th style="width: 5% ..."> URL </th>
        <th style="width: 1% ..."> Approval Status </th>
       <!--  <th style="width: 5% ..."> Action1 </th>
        <th style="width: 5% ..."> Action2 </th> -->
      </tr>
    </thead>
     <tbody>
       {% for row in variable.data %}    
            <tr class='table_body'>
                <td><input type="checkbox" name="multiselect"></td>
                <td >{{row[3]}}</td>
                <td >{{row[14]}}</td>
                <td >{{row[19]}}</td>
                <td >{{row[22]}}</td>
                <td >{{row[20]}}</td>
                <td >{{row[21]}}</td>
                <td> <a href = "{{row[4]}}" target="_blank" data-toggle="tooltip" title= {{row[4]}}>{{row[4]}}</td>
                <td>{{row[18]}}</td>
                <!-- td ><p  class="btn btn-primary btn-sm runbtn edit">Edit</p></td>
                <td ><p  class="btn btn-primary btn-sm runbtn">Delete</p></td> -->
            </tr>
        {% endfor %}
    </tbody>
  </table>
  <p  class="btn btn-primary btn-sm runbtn prevpage" id= 'prev'><i class="fa fa-arrow-left"></i></p>
<p  class="btn btn-primary btn-sm runbtn nextpage"><i class="fa fa-arrow-right"></i></p>

  <div class="modal fade" id="myModal" role="dialog">
    <div class="modal-dialog modal-lg">
    
      <!-- Modal content-->
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal">&times;</button>
        </div>
        <div class="modal-body"id="edit_bdy">
          
        </div>
        <div class="modal-footer">
          <button type="submit" onclick="Update()" id="submit1" class="btn btn-primary">Save Changes</button>
          <button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>
        </div>
      </div>
      
    </div>
  </div>
  
                </div>
              </div>
            </div>
      </div>
    </div>
  </div>
  <script>
    $(document).ready(function() {
        // code to read selected table row cell data (values).
        $(".edit").on('click', function() {
          console.log('clicked')
            // get the current row
            var currentRow = $(this).closest("tr");
            var tds = currentRow.find("td");
            console.log(tds[0]);
            var str = `<form  action = "update.php" method="POST" id="editform"><div class='form-group'>
                        <label>Sno</label>
                        <input name = "up_hrid" type='text' disabled  class='form-control edit_db' value = '` + $(tds[0]).text() + `'>
                    </div>
                    <div class='form-group'>
                        <label>Date</label>
                        <input name ='Domain' type='text' class='form-control edit_db'  value='` + $(tds[1]).text() + `'>
                    </div>
                    <div class='form-group'>
                        <label>Article Heading</label>
                        <input name ='Required' type='text' class='form-control edit_db'  value='` + $(tds[2]).text() + `'>
                    </div>
                    <div class='form-group'>
                        <label>Article Text</label>
                        <textarea name ='Date' type='text' class='form-control edit_db' rows="8">` + $(tds[3]).text() + `</textarea>
                    </div>
                    <div class='form-group'>
                        <label>Keyword1</label>
                        <input name ='Priority' type='text' class='form-control edit_db'  value='` + $(tds[4]).text() + `'>
                    </div>
                    <div class='form-group'>
                        <label>Keyword2 </label>
                        <input name ='Min_Exp' type='text' class='form-control edit_db'  value='` + $(tds[5]).text() + `'>
                    </div>
                    <div class='form-group'>
                        <label>Keyword3 </label>
                        <input name ='Min_Exp' type='text' class='form-control edit_db'  value='` + $(tds[6]).text() + `'>
                    </div>
                    </form>
                    
                    `;
            $('#edit_bdy').html(str);
            $('#myModal').modal('show');
        });
     });
</script>

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
<script type="text/javascript">
  function logout(){
    var r = confirm(" {{variable.username}} , Are you sure you want to logout")
    if(r == true){
      window.location.replace('/logout')
      console.log('true');
    }
    else{
      window.location.replace('/Edit')
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
  }
  var pg= '{{variable.pgid}}'
  if(pg == '0'){
    $('.prevpage').hide();
  }
  if('{{variable.valid}}' == 'invalidfile' ){
    console.log('invalid');
    alert("Coloumn headers in Uploaded file didn't match or You have selected wrong website list. Please try again");
  }
  if('{{variable.valid}}' == 'validfile'){
    alert('File Uploaded successfully');
  }
  if('{{variable.valid}}' == 'invalidwebsite'){
    alert('You have selected wrong website list. Please try again');
  }

  if('{{variable.valid}}' == 'articlenotfound'){
    alert('Article not found');
  }
}
</script>
<script type="text/javascript">
  $(document).ready(function() {
    $(".prevpage").on('click', function() {
      console.log('clicked')
      var value1 = '{{variable.pgid}}'
      var value = '{{variable.value}}'
      value1 = parseInt(value1) - 10
      window.location.replace('/Display?id='+value+'&pgno='+value1)
    });
  });
</script>
<script type="text/javascript">
         // Select all check boxes : Setting the checked property to true in checkAll() function
           function checkAll(){
             var items = document.getElementsByName('multiselect');
               for (var i = 0; i < items.length; i++) {
                   if (items[i].type == 'checkbox')
                       items[i].checked = true;
               }
           }
         // Clear all check boxes : Setting the checked property to false in uncheckAll() function
           function uncheckAll(){
             var items = document.getElementsByName('multiselect');
               for (var i = 0; i < items.length; i++) {
                   if (items[i].type == 'checkbox')
                       items[i].checked = false;
               }
           }
      </script>
<script type="text/javascript">
  $(document).ready(function() {
    $(".prevpage").on('click', function() {
      console.log('clicked')
      var value1 = '{{variable.pgid}}'
      var value = '{{variable.value}}'
      if(value1 == '0'){
        $('#prev').hide();
      }
      else{
         value1 = parseInt(value1) - 10
         window.location.replace('/Display?id='+value+'&pgno='+value1+'&valid=nofile')
      }
    });
  });
</script>
<script type="text/javascript">
  $(document).ready(function() {
    $(".nextpage").on('click', function() {
      console.log('clicked')
      var value1 = '{{variable.pgid}}'
      var value = '{{variable.value}}'
      value1 = parseInt(value1) + 10
      window.location.replace('/Display?id='+value+'&pgno='+value1+'&valid=nofile')
    });
  });
</script>
<script type="text/javascript">
      $(".Downexcel").on('click', function() {
      var webid = '{{variable.pgid}}'
      var webname = '{{variable.value}}'
      window.location.replace('/Download_singlepage_file?webname='+webname+'&webid='+webid)
    });
</script>
</body>

</html>
