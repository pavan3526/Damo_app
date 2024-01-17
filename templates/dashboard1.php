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
    height: 40px;
  }
  .db2{
    padding: 10px;
  }
  td {
    max-width: 100px !important;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .analysttable{
    padding-top: 20px;
  }
 /*  .usertype{
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
           <div class="topnav analystnav">
                        <a href="/Scraper">Scraper</a>
                        <a class="actived" href="/View">View / Edit data</a>
                        <a href="/ChangePassword">Change Password</a>
                        <a href="/users_page" class='users'>Users</a>
                        <a href="/downloadstab" class='Notification'>Downloads</a>
                      </div>
        <div class = "row">
              <p class="usertype"> {{variable.usertype}} </p>
              <a type="submit" onclick="logout()" data-toggle="tooltip" title= {{variable.username}} ><i class="fa fa-power-off poweroff logout" aria-hidden="true"></i></a>
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
                        <!--   <button class="btn btn-info runbtn select1" type="button" id="dropdownmenu" data-toggle="dropdown" aria-haspopup="false" aria-expanded="false">Select by Name of the Organization</button>
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
                          <!-- <p class="btn btn-primary btn-sm runbtn approval">Approve</p> -->
                    <div class = 'row'>
                           <p class="subhead"><b> Website Name : </b> {{variable.value}} </p>
                           <p class="subhead"><b> No of Articles : </b> {{variable.articlecount}} </p>

                          <div class='fourbtn'>
                          <!-- <p class="btn btn-primary btn-sm runbtn approval">Approve</p> -->
                          <div class='row'>
                          <p  class="btn btn-primary btn-sm runbtn approval">Request to Approval</p>&nbsp
                          <p  class="btn btn-primary btn-sm runbtn Downexcel">Download this page</p>&nbsp
                          <form enctype="multipart/form-data" method='POST' action='/fileupload1' id='upfile'>
                              <label for='file-upload' class='btn btn-primary btn-sm runbtn Upexcel' type='button'>
                              <span>Upload Excel</span>
                              <input type="file" id='file-upload' name='file' onchange="this.form.submit()" class='fileupload'/>
                              <input type='text' value = '{{variable.value}}' name ='webname' style="display: none;">
                              <input type='text' value = '{{variable.pgid}}' name ='pgid' style="display: none;">
                          </form>
                        </div>
                        </div>
                        </div>
                      </div>
                    </div>
                    <div class="row">
                      <div class='DC'>
                         <button type="button" value="selectAll" class="btn btn-primary btn-sm runbtn main" onclick="checkAll()">Select all</button>
                                <button type="button" value="Deleteall" class=" btn btn-primary btn-sm runbtn Deletemultiple">Delete</button>

                <button type="button" value="deselectAll" class="btn btn-primary btn-sm runbtn main" onclick="uncheckAll()">Unselect all</button>
              </div>
                        </div>


                </div>
                <div class='row'>
                <p class="subhead"><b> No of pages : </b> {{variable.noofpages}} </p>
                <form class="form-inline"  action="/arsearch" method="POST">
                  <div class="form-group">
                    <input class="form-control an_search" id="asearch" name='asearch' placeholder="Enter page Number" type="text">
                  </div>
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


                    <div class="table-responsive analysttable">
                    <table class="table table-hover table-bordered table-striped " id="webdata">
    <thead>
      <tr class="table_head" >
        <th style="width: 1% ..."> Select</th>
        <th style="width: 5% ...">Article ID</th>
        <th style="width: 1% ...">Date</th>
        <th style="width: 2% ...">Healthcare Enterprise</th>
        <th style="width: 1% ...">Technology</th>
        <th style="width: 1% ...">Use Cases</th>
        <th style="width: 5% ...">Vendor</th>
        <th style="width: 1% ..."> URL </th>
        <th style="width: 1% ..."> Approval Status </th>
        <th style="width: 1% ..."> Edit </th>
        <th style="width: 1% ..."> Delete </th>
      </tr>
    </thead>
     <tbody>
       {% for row in variable.data %}    
            <tr  class="content">
                <td><input type="checkbox" name="multiselect"></td>
                <td >{{row[3]}}</td>
                <td >{{row[14]}}</td>
                <td >{{row[19]}}</td>
                <td >{{row[22]}}</td>
                <td >{{row[20]}}</td>
                <td >{{row[21]}}</td>
                <td> <a href = "{{row[4]}}" target="_blank" data-toggle="tooltip" title= {{row[4]}}>{{row[4]}}</td>
                <td >{{row[18]}}</td>
                <td ><p  class="btn btn-primary btn-sm runbtn edit">Edit</p></td>
                <td ><p  class="btn btn-primary btn-sm runbtn Delete">Delete</p></td>
            </tr>
        {% endfor %}
    </tbody>
  </table>
  </table>
  <p  class="btn btn-primary btn-sm runbtn prevpage " id= 'prev'><i class="fa fa-arrow-left"></i></p>
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
          <!-- <button type="submit" onclick="Update()" id="submit1" class="btn btn-primary">Save Changes</button> -->
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
        $(".edit").on('click', function() {
          console.log('clicked')
          var currentRow = $(this).closest("tr");
          var tds = currentRow.find("td");
          console.log(tds[0]);
          var value = $(tds[1]).text();
          var value1 = '{{variable.value}}'
          $.ajax({
            url: '/edit_row',
            type:'POST',
            data : JSON.stringify({'data': value,'data1':value1}),
            contentType: "application/json",
            success: function(response){
            console.log(response['sucess'][0])
              console.log(response['sucess'][0])
              var heading = response['sucess'][0]
              var text = response['sucess'][1]
              var date = response['sucess'][2]
              var articleid = response['sucess'][10]
              var Technology = response['sucess'][3]
              var broad_use_case = response['sucess'][4] 
              var health_system = response['sucess'][5] 
              var vendor = response['sucess'][6] 
              var vendor_product = response['sucess'][7] 
              var speciality = response['sucess'][8]
              var article_url = response['sucess'][9]
              var section_type = response['sucess'][11]

              var str = `<form action="/Savechanges" method="POST"><div class='row'><div class="col-sm-6">
                          <div class='form-group'>
                        <label>Article ID</label>
                      <input name = "aid" type='text' readonly  class='form-control edit_db' value = '` + articleid  + `'>
                  </div>
                  <div class='form-group'>
                      <label>Article date</label>
                      <input name ='date' type='text' class='form-control edit_db'  value='` + date + `'>
                  </div>
                  <div class='form-group'>
                      <label>Article Heading</label>
                      <input name ='heading' type='text' class='form-control edit_db'  value='` + heading + `'>
                  </div>
                  <div class='form-group'>
                      <label>Technology Category </label>
                      <input name ='Technology' type='text' class='form-control edit_db'  value='` + Technology + `'>
                  </div>
                  <div class='form-group'>
                      <label>Healthcare Enterprise </label>
                      <input name ='health_system' type='text' class='form-control edit_db'  value='` + health_system + `'>
                  </div>
                  </div>
                  <div class="col-sm-6">
                  <div class='form-group'>
                      <label>Use cases </label>
                      <input name ='broad_use_case' type='text' class='form-control edit_db'  value='` + broad_use_case + `'>
                  </div>
                  <div class='form-group'>
                      <label>Vendor</label>
                      <input name ='vendor' type='text'  class='form-control edit_db'  value='` + vendor+ `'>
                  </div>
                  <div class='form-group'>
                      <label>Vendor Product </label>
                      <input name ='vendor_product' type='text'  class='form-control edit_db'  value='` + vendor_product + `'>
                  </div>
                  <div class='form-group'>
                      <label>Speciality </label>
                      <input name ='speciality' type='text'  class='form-control edit_db'  value='` + speciality + `'>
                  </div>
                  <div class='form-group'>
                      <label>Article URL </label>
                      <input name ='article_url' type='text'  class='form-control edit_db'  value='` + article_url + `'>
                  </div>
                  <div class='form-group'>
                      <label>Website Name </label>
                      <input name ='webname' type='text' readonly class='form-control edit_db'  value='` + value1 + `'>
                  </div>
                  <input type='text' value='` + section_type + `' name ='webname1' style="display: none;">
                  <input type='text' value = '{{variable.value}}' name ='webname1' style="display: none;">
                  <input type='text' value = '{{variable.pgid}}' name ='pgid1' style="display: none;">
                  </div>
                  </div>
                   <div class='form-group'>
                      <label>Article Text</label>
                      <textarea name ='text' type='text' class='form-control edit_db' rows="8">` + text + `</textarea>
                  </div>
                  <button type="submit"  name="submit" class="btn btn-primary btn-sm runbtn">Save changes</button>
                  </form>    `;
                  $('#edit_bdy').html(str);
                  $('#myModal').modal('show');
                },
              
                error: function(error){
                  console.log('U have done error')
                  console.log(error);
                }
              });
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
    alert('Uploaded file is invalid');
  }
  if('{{variable.valid}}' == 'validfile'){
    alert('File Uploaded successfully');
  }
  if('{{variable.valid}}' == 'articlenotfound'){
    alert('Article not found');
  }
   if('{{variable.valid}}' == 'invalidwebsite'){
    alert('Uploaded file is having other website data');
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
  $(document).ready(function() {
    $(".nextpage").on('click', function() {
      console.log('clicked')
      var value1 = '{{variable.pgid}}'
      var value = '{{variable.value}}'
      value1 = parseInt(value1) + 10
      window.location.replace('/Display?id='+value+'&pgno='+value1)
    });
  });
</script>
<script type="text/javascript">
  $('.Delete').on('click',function(){
    console.log('clicked')
    var currentRow = $(this).closest("tr");
    var tds = currentRow.find("td");
    console.log(tds[0]);
    var value = $(tds[1]).text();
    var value1 = '{{variable.value}}'
    var pg = '{{variable.pgid}}'
    var del = confirm('Are you sure want to suggest to delete '+value)
    if (del == true){
      $.ajax({
        url: '/Delete_single',
        type:'POST',
        data : JSON.stringify({'data': value,'data1':value1}),
        contentType: "application/json",
        success: function(response){
          alert(value + 'successfully suggested to delete')
          console.log(response['success'])
          window.location.replace('/Display?id='+value1+'&pgno='+pg+'&valid=nofile')
        },
        error: function(error){
          console.log('U have done error')
          console.log(error);
        }
      });
    }
    else{
      window.location.replace('/Display?id='+value1+'&pgno='+pg+'&valid=nofile')
    }
  });
</script>
 <script type="text/javascript">
  var message = ''
  var weblist = []
  $('.Deletemultiple').on('click',function(){
    $("#webdata input[type=checkbox]:checked").each(function () {
      var currentRow = $(this).closest("tr");
      var tds = currentRow.find("td");
      var value = $(tds[1]).text();
      weblist.push(value);
      console.log(value);
      var $td = $(this).closest('td');
    });
    var value1 = '{{variable.value}}'
    var pg = '{{variable.pgid}}'
    console.log(weblist);
    if(weblist.length == 0){
      alert('No Articles are selected')
    }
    else{
      var del = confirm('Do you want to suggest to delete articles '+weblist);
    if(del == true){
      $.ajax({
        url: '/Delete_multiple',
        type:'POST',
        data : JSON.stringify({'data': weblist,'data1':value1}),
        contentType: "application/json",
        success: function(response){
          alert(weblist+' successfully suggested to delete')
          window.location.replace('/Display?id='+value1+'&pgno='+pg+'&valid=nofile')
        },
        error: function(error){
          console.log('U have done error')
          console.log(error);
        }
      });
    }
    else{
      window.location.replace('/Display?id='+value1+'&pgno='+pg+'&valid=nofile')
    }
    }
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
  var message = ''
  var weblist = []
  $('.approval').on('click',function(){
    $("#webdata input[type=checkbox]:checked").each(function () {
      var currentRow = $(this).closest("tr");
      var tds = currentRow.find("td");
      var value = $(tds[1]).text();
      weblist.push(value);
      console.log(value);
      var $td = $(this).closest('td');
    });
    var value1 = '{{variable.value}}'
    var pg = '{{variable.pgid}}'
    console.log(weblist);
    if(weblist.length == 0){
      alert('No Articles are selected')
    }
    else{
      var del = confirm('Do you want to request for approve articles '+weblist);
    if(del == true){
      $.ajax({
        url: '/Approve',
        type:'POST',
        data : JSON.stringify({'data': weblist,'data1':value1}),
        contentType: "application/json",
        success: function(response){
          alert(weblist+' successfully sent for request of approval')
          window.location.replace('/Display?id='+value1+'&pgno='+pg+'&valid=nofile')
        },
        error: function(error){
          console.log('U have done error')
          console.log(error);
        }
      });
    }
    else{
      window.location.replace('/Display?id='+value1+'&pgno='+pg+'&valid=nofile')
    }

    }
  });
</script>
</body>

</html>
