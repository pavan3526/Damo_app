<!DOCTYPE html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>Damo Dashboard</title>
  <!-- <link rel="stylesheet" href="css/style.css"> -->
  <link rel="stylesheet"  href="{{ url_for('static', filename='css/style.css') }}">
  <!-- endinject -->
  <link rel="shortcut icon" href="images/favicon.png" />
  <!-- <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css"> -->
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
  .db2{
    padding: 10px;
  }
  td {
    max-width: 100px !important;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .producttb{
    padding-top: 30px;
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
           <div class=" topnav productnav">
                        <a href="/Scraper">Scraper</a>
                        <a href="/View">View / Edit data</a>
                        <a href="/ChangePassword">Change Password</a>
                        <a href="/users_page" class='users'>Users</a>
                        <a class="actived" href="/Production_tab?pgno=0" class='production'>Production</a>
                        <a href="/Notification_tab?pgno=0" class='Notification'>Notifications</a>
                        <a href="/keywords?valid=nofile" class='Keywords'>Keywords</a>
                        <a href="/downloadstab" class='Notification'>Downloads</a>
                      </div>
        <div class = "row">
              <p class="usertype"> {{variable.usertype}} </p>
              <a type="submit" onclick="logout()" data-toggle="tooltip" title= {{variable.username}} ><i class="fa fa-power-off" id="logout" aria-hidden="true"></i></a>
        </div>
      </div>
    </nav>
        <div class="container-fluid page-body-wrapper">
      <div class="main-panel">
        <div class="content-wrapper">
          <div class="row">
            <div class="col-lg-12 grid-margin stretch-card">
              <div class="card db2">
                <div class="card-body">
                   <div class="form-group">
                      <div class="row">
                        <div class="dropdown">
                       <!--    <button class="btn btn-info runbtn select1" type="button" id="dropdownmenu" data-toggle="dropdown" aria-haspopup="false" aria-expanded="false">Select by Name of the Organization</button>
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
                          <div class = 'row'>
                          <p class="subhead"> <b> Production Table </b> </p>
                        <!--   <div class='fourbtn'>
                          <p class="btn btn-primary btn-sm runbtn approval">Approve</p>
                          <p  class="btn btn-primary btn-sm runbtn Production">Move to Production</p>
                          <p  class="btn btn-primary btn-sm runbtn Downexcel">Download in Excel</p>
                           <form enctype="multipart/form-data" method='POST' action='/fileupload' id='upfile'>
                            <div class="uploadfile">
                              <input type="file" id='file' name='file' class='fileupload'/>
                              <button type='submit' class="btn btn-primary btn-sm runbtn Upexcel">Upload Excel</button>
                              <input type='text' value = '{{variable.value}}' name ='webname' style="display: none;">
                              <input type='text' value = '{{variable.pgid}}' name ='pgid' style="display: none;">
                            </div>
                          </form>
                        </div> -->
                        </div>
                        </div>
                      </div>
                    </div>
                    <div class="row">
                      <div class='DC'>
                         <button type="button" value="selectAll" class="btn btn-primary btn-sm runbtn main" style="height: 35px;" onclick="checkAll()">Select all</button>
                                <button type="button" value="Deleteall" class=" btn btn-primary btn-sm runbtn Deletemultiple" style="height: 35px;">Delete</button>

                <button type="button" value="deselectAll" class="btn btn-primary btn-sm runbtn main" style="height: 35px;" onclick="uncheckAll()">Clear</button>
              </div>

                <div class = 'row'>
                          <!-- <p class="subhead"><b> Website Name : </b> {{variable.value}} </p> -->

                          <div class='fourbtn'>
                          <div class="row">
                          <p  class="btn btn-primary btn-sm runbtn Download_all">Download entire table </p>&nbsp&nbsp
                          <p  class="btn btn-primary btn-sm runbtn Downexcel">Download this page</p>&nbsp&nbsp
                           <form enctype="multipart/form-data" method='POST' action='/fileupload2' id='upfile'>
                              <label for='file-upload' class='btn btn-primary btn-sm runbtn Upexcel' type='button'>
                              <span>Upload Excel</span>
                              <input type="file" id='file-upload' name='file' onchange="this.form.submit()" class='fileupload'/>
                              <input type='text' value = 'production_table' name ='webname' style="display: none;">
                              <input type='text' value = '{{variable.pgid}}' name ='pgid' style="display: none;">
                          </form>
                        </div>
                        </div>


              </div>
                </div>
                <div class='row'></div>
                  <div class="table-responsive producttb">
                    <table class="table table-hover table-bordered table-striped " id="webdata">
    <thead>
      <tr class="table_head" >
        <th style="width: 1% ..."> Select</th>
        <th style="width: 1% ..."> Website name</th>
        <th style="width: 5% ...">Article ID</th>
        <th style="width: 1% ...">Date</th>
        <th style="width: 2% ...">Healthcare Enterprise</th>
        <th style="width: 1% ...">Technology Category </th>
        <th style="width: 1% ...">Use Case</th>
        <th style="width: 5% ...">Vendor</th>
        <th style="width: 1% ..."> URL </th>
        <th style="width: 1% ..."> Edit </th>
        <th style="width: 1% ..."> Delete </th>
      </tr>
    </thead>
     <tbody>
       {% for row in variable.data %}    
            <tr  class="content">
                <td><input type="checkbox" name="multiselect"></td>
                <td >{{row[18]}}</td>
                <td >{{row[3]}}</td>
                <td >{{row[14]}}</td>
                <td style="width: 2% ...">{{row[19]}}</td>
                <td >{{row[22]}}</td>
                <td >{{row[20]}}</td>
                <td >{{row[21]}}</td>
                <td> <a href = "{{row[4]}}" target="_blank" data-toggle="tooltip" title= {{row[4]}}>{{row[4]}}</td>
                <td ><p  class="btn btn-primary btn-sm runbtn edit">Edit</p></td>
                <td ><p  class="btn btn-primary btn-sm runbtn Delete">Delete</p></td>
            </tr>
        {% endfor %}
    </tbody>
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
          var value = $(tds[2]).text();
          var value1 = 'production_table'
          $.ajax({
            url: '/edit_row',
            type:'POST',
            data : JSON.stringify({'data': value,'data1':value1}),
            contentType: "application/json",
            success: function(response){
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

              var str = `<form action="/Savechanges_production" method="POST"><div class='row'><div class="col-sm-6">
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
                      <label>Health System </label>
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
                  <input type='text' value = '{{variable.pgid}}' name ='pgid1' style="display: none;">
                  </div>
                  </div>
                   <div class='form-group'>
                      <label>Article Text</label>
                      <textarea name ='text' type='text' class='form-control edit_db' rows="8">` + text + `</textarea>
                  </div>
                  <button type="submit"  name="submit" class="btn btn-primary btn-sm runbtn">Save changes</button>
                  </form>
                  `;
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

<!-- <script type="text/javascript">
    $('.Save').on('click', function(){
      var form1 = $(#editform).serialize()
      console.log(form1)
      console.log('click')
    });
</script> -->
<script type="text/javascript">
  function logout(){
    var r = confirm(" {{variable.username}} , Are you sure you want to logout")
    if(r == true){
      window.location.replace('/logout')
      console.log('true');
    }
    else{
      window.location.replace('/Production_tab')
    }
  }
</script>
<script type="text/javascript">
  $(document).ready(function() {
    $(".prevpage").on('click', function() {
      console.log('clicked')
      var value1 = '{{variable.pgid}}'
      if(value1 == '0'){
        $('#prev').hide();
      }
      else{
         value1 = parseInt(value1) - 10
         window.location.replace('/Production_tab?pgno='+value1)
      }
    });
  });
</script>
<script type="text/javascript">
  $(document).ready(function() {
    $(".nextpage").on('click', function() {
      console.log('clicked')
      var value1 = '{{variable.pgid}}'
      value1 = parseInt(value1) + 10
      window.location.replace('/Production_tab?pgno='+value1)
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
}
</script>
<script type="text/javascript">
      $(".Downexcel").on('click', function() {
      var webid = '{{variable.pgid}}'
      var webname = 'production_table'
      window.location.replace('/Download_singlepage_file_production?webname='+webname+'&webid='+webid)
    });
</script>
<script type="text/javascript">
  $('.Delete').on('click',function(){
    console.log('clicked')
    var currentRow = $(this).closest("tr");
    var tds = currentRow.find("td");
    console.log(tds[0]);
    var value = $(tds[2]).text();
    // var websitename = $(tds[2]).text();
    var value1 = 'production_table'
    var pg = '{{variable.pgid}}'
    var del = confirm('Are you sure want to delete '+value)
    if (del == true){
      $.ajax({
        url: '/Delete_single',
        type:'POST',
        data : JSON.stringify({'data': value,'data1':value1}),
        contentType: "application/json",
        success: function(response){
          alert(value + 'successfully got deleted')
          console.log(response['success'])
          window.location.replace('Production_tab?pgno='+pg)
        },
        error: function(error){
          console.log('U have done error')
          console.log(error);
        }
      });
    }
    else{
      window.location.replace('Production_tab?pgno='+pg)
    }
  });
</script>
 <script type="text/javascript">
  var message = ''
  var weblist = []
  var orglist = []
  $('.Deletemultiple').on('click',function(){
    $("#webdata input[type=checkbox]:checked").each(function () {
      var currentRow = $(this).closest("tr");
      var tds = currentRow.find("td");
      var value = $(tds[2]).text();
      weblist.push(value);
      // var websitename = $(tds[2]).text();
      // orglist.push(websitename)
      console.log(value);
      var $td = $(this).closest('td');
    });
    var value1 = 'production_table'
    var pg = '{{variable.pgid}}'
    console.log(weblist);
    if(weblist.length == 0){
      alert('No articles are selected')
    }
    else{
      var del = confirm('Do you want to delete articles '+weblist);
    if(del == true){
      $.ajax({
        url: '/Delete_multiple',
        type:'POST',
        data : JSON.stringify({'data': weblist,'data1':value1}),
        contentType: "application/json",
        success: function(response){
          alert(weblist+' successfully got deleted')
          window.location.replace('/Production_tab?pgno='+pg)
        },
        error: function(error){
          console.log('U have done error')
          console.log(error);
        }
      });
    }
    else{
      window.location.replace('/Production_tab?pgno='+pg)
    }

    }
  });
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
    var del = confirm('Do you want to approve articles '+weblist);
    if(del == true){
      $.ajax({
        url: '/Approve',
        type:'POST',
        data : JSON.stringify({'data': weblist,'data1':value1}),
        contentType: "application/json",
        success: function(response){
          alert(weblist+' successfully got Approved')
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
  $('.Production').on('click',function(){
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
    var del = confirm('Do you want to send articles '+weblist+' to production');
    if(del == true){
      $.ajax({
        url: '/Production',
        type:'POST',
        data : JSON.stringify({'data': weblist,'data1':value1}),
        contentType: "application/json",
        success: function(response){
          alert(weblist+' successfully sent to Production')
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
function filterText()
  {  
    var rex = new RegExp($('#filterText').val());
    if(rex =="/all/"){clearFilter()}else{
      $('.content').hide();
      $('.content').filter(function() {
      return rex.test($(this).text());
      }).show();
  }
  }
  
function clearFilter()
  {
    $('.filterText').val('');
    $('.content').show();
  }
</script>
<script type="text/javascript">
    $('.Download_all').on('click', function(){
      console.log('clicked')
      var value = 'production_table'
      alert(value+ ' Accepted list scheduled to download')
      $.ajax({
        url: '/Download_file_production',
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

<!-- <script type="text/javascript">
  $('.Upexcel').on('click',function(){
    $('#file').show()
    console.log('clickest')
});
</script> -->
</body>

</html>
