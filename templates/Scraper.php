<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <!-- <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"> -->
  <meta name="viewport" content="width=device-width, initial-scale=1">
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

  <!-- jQuery Datatable js -->



 <style type="text/css">
  .logo1{
    width : 200px;
    height : 60px;
  }
 
 </style>
</head>
<body onload="Pageload()">
  <div class="container-scroller">
    <nav class="navbar col-lg-12 col-12 p-0 fixed-top d-flex flex-row">
      <div class="text-center navbar-brand-wrapper d-flex align-items-center justify-content-center">
        <img src="{{url_for('static', filename='logo.png')}}" class='image' align="middle">

      </div>
      <div class="navbar-menu-wrapper d-flex align-items-center justify-content-end">
           <div class="topnav scrapernav">
                        <a class="actived" href="/Scraper">Scraper</a>
                        <a href="/View">View / Edit data</a>
                        <a href="/ChangePassword">Change Password</a>
                        <a href="/users_page" class='users'>Users</a>
                        <a href="Production_tab?pgno=0" class='production'>Production</a>
                        <a href="/Notification_tab?pgno=0" class='Notification'>Notifications</a>
                        <a href="/keywords?valid=nofile" class='Keywords'>Keywords</a>
                        <a href="/downloadstab" class='Downloads'>Downloads</a>
                      </div>
        
              <p class="usertype"> {{variable.usertype}} </p>
              <a type="submit" onclick="logout()" data-toggle="tooltip" title= {{variable.username}} ><i class="fa fa-power-off scraperpoweroff" aria-hidden="true"></i></a>
      </div>
    </nav>
    <!-- partial -->
        <div class="container-fluid page-body-wrapper">
      <div class="main-panel">
        <div class="content-wrapper">
          <div class="row">
            <div class="col-lg-16 grid-margin stretch-card">
              <div class="card">
                <div class="card-body">
                  <div class="row">
                    <label for="Website" class="web">Website Listing</label>
                    <input type="text" name = "Website" class="form-control" style="width:300px;" id="navbar-search-input" placeholder="Search Website.." aria-label="search" aria-describedby="search">
                  </div>
                  <div class="row">
                    <div class="firstelements">
                    <!-- <button type="button" value="deselectAll" class="btn btn-primary btn-sm runbtn main" onclick="uncheckAll()">Clear</button> -->
                    <input class="btn btn-primary btn-sm runbtn Multirefresh" type="button" value="Multi-refresh"></input>
                    <input class="btn btn-primary btn-sm runbtn reset" type="button" value="Reset Status"></input>
                      <label for="filterText" class="selectlabel"><b>Select by Status: </b></label>
                        <select id='filterText' class="form-control" style='display:inline-block' onchange='filterText()'>
                        <option disabled selected>Select</option>
                        <option value='all'>All</option>
                        <option value='Need to Scrape'>Need to Scrape</option>
                        <option value='In Queue'>In Queue</option>
                        <option value='In progress'>In progress</option>
                        <option value='Completed'>Completed</option>
                      </select>
                  </div>
                  </div>
                  <div class="table-responsive">
                    <table class="table table-hover " id = 'websitelist'>
    <thead>
      <tr>
        <th>Select</th>
        <th>Website Name</th>
        <th>New Refreshed Articles </th>
        <th>Type</th>
        <th>Last Refreshed on </th>
        <th>Requires Refresh</th>
        <th>Refresh Status</th>
        <th>Execute script</th>
      </tr>
    </thead>
    <tbody>
       {% for row in variable.data %}
            <tr class="content">
                <td><input type="checkbox" name="refresh"></td>
                <td>{{row[6]}}</td>
                <td>{{row[17]}}</td>
                <td>{{row[4]}}</td>
                <td>{{row[14]}}</td>
                <td>{{row1}}</td>
                <td>{{row[16]}}</td>
                <td><input class="btn btn-primary btn-sm runbtn refresh" type="button" id="{{row[6]}}" value="Refresh"></input></td>
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
      window.location.replace('/dashboard')
    }
  }
</script>

<script type="text/javascript">
function Pageload() {
  // $('#websitelist_length').hide();
  $('#websitelist_filter').hide();
  $('#websitelist_length').hide();
  // $('.refreshing').hide();
  // console.log('Approver');
  // if('{{variable.usertype}}' == 'Admin'){
  //   $('#Edit').hide();
  // }
  if('{{variable.username}}' == ''){
    window.location.replace('/login')
  }
  if('{{variable.usertype}}' != 'Superadmin' && '{{variable.usertype}}' != 'Admin' ){
    $('.users').hide();
  }
  if('{{variable.usertype}}' != 'Superadmin' && '{{variable.usertype}}' != 'Approver' ){
    $('.production').hide();
    $('.Notification').hide();
    $('.Keywords').hide();
  }
  if('{{variable.usertype}}' == 'Superadmin' || '{{variable.usertype}}' == 'Approver'){
    $.ajax({
      url: '/Notifystatus',
      type:'POST',
      data : JSON.stringify({'data': 'Notification'}),
      contentType: "application/json",
      success: function(response){
        console.log(response['status'])
        if(response['status'] != 1){
          alert('Hi, {{variable.username}} you have got '+response['status']+' articles to approve.')
        }
        else if(response['status'] == 1){
          alert('Hi, {{variable.username}} you have got '+response['status']+' article to approve.')
        }
      },
      error: function(error){
        console.log('U have done error')
        console.log(error);
      }
    });
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
         // Select all check boxes : Setting the checked property to true in checkAll() function
           function checkAll(){
             var items = document.getElementsByName('refresh');
               for (var i = 0; i < items.length; i++) {
                   if (items[i].type == 'checkbox')
                       items[i].checked = true;
               }
           }
         // Clear all check boxes : Setting the checked property to false in uncheckAll() function
           function uncheckAll(){
             var items = document.getElementsByName('refresh');
               for (var i = 0; i < items.length; i++) {
                   if (items[i].type == 'checkbox')
                       items[i].checked = false;
               }
           }
      </script>
<!-- <script type="text/javascript">
  $(document).ready( function () {
    $('#websitelist').DataTable();
} );
</script> -->

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
<script type="text/javascript">
  $(document).ready( function () {
    $('.refresh').on('click', function(){
      console.log('clicked')
      var currentRow = $(this).closest("tr");
      var tds = currentRow.find("td");
      var value = $(tds[1]).text();
      $('.refresh').prop('disabled', true);
      $('.Multirefresh').prop('disabled',true);
      var $td = $(this).closest('td');
      $td.find($(':button[value="Refresh"]')).prop("value", "Inprogress");
      $.ajax({
        url: '/Multirefreshstep1',
        type:'POST',
        data : JSON.stringify({'data': value}),
        contentType: "application/json",
        success: function(response){
          $('.refresh').prop('disabled', true);
          $('.Multirefresh').prop('disabled',true);
          console.log(response['values']);
          if(response['flag'] == 'cantscrape'){
            alert('Cant scrape the data, because already other websites are in progress to scrape')
          }
          else{
            $.ajax({
              url: '/Scrapeit_Single',
              type:'POST',
              data : JSON.stringify({'data': value}),
              contentType: "application/json",
              success: function(response){
                console.log(response['status'])
                $('.Multirefresh').prop('disabled',true);
                $('.refresh').prop('disabled', false);
                $td.find($(':button[value="Inprogress"]')).prop("value", "Refresh");
              },
              error: function(error){
                console.log('U have done error')
                console.log(error);
              }
            });
          }
      },
      error: function(error){
        console.log('U have done error')
        console.log(error);
      }
    });
    // let st = setInterval(() => {
    //   $.ajax({
    //     type:'POST',
    //     url: '/Status',
    //     data : JSON.stringify({'data': value}),
    //     contentType: "application/json",
    //     error: function(error){
    //       console.log('U have done error')
    //       console.log(error);
    //     },
    //     success: function(response2){
    //       console.log('instant response '+ (response2.status))
    //       var output = response2.status;
    //       console.log(typeof(output))
    //       if(output == 'Completed'){
    //         clearInterval(st)
    //         alert('Refresh done successfully')
    //       }
    //     },
    //   });
    // },1000);
   });
  });
</script>
<script type="text/javascript">
  $('#websitelist input[type=checkbox]').on('change', function (e) {
      if ($('#websitelist input[type=checkbox]:checked').length > 10) {
        $(this).prop('checked', false);
      }
  });
  $('.Multirefresh').on('click', function(){
    var message = ''
    var weblist = []
    $("#websitelist input[type=checkbox]:checked").each(function () {
      var currentRow = $(this).closest("tr");
      var tds = currentRow.find("td");
      var value = $(tds[1]).text();
      weblist.push(value);
      console.log(value);
      console.log(typeof(value))
      var $td = $(this).closest('td');
      // $('.#'+value).prop("value", "Inprogress");
    });
    console.log(weblist);
    alert('Initializing');
    $.ajax({
      url: '/Multirefreshstep1',
      type:'POST',
      data : JSON.stringify({'data': weblist}),
      contentType: "application/json",
      success: function(response){
        $('.refresh').prop('disabled', true);
        $('.Multirefresh').prop('disabled',true);
        console.log(response['values']);
        $.ajax({
          url: '/Scrapeit',
          type:'POST',
          data : JSON.stringify({'data': weblist}),
          contentType: "application/json",
          success: function(response){
            $('.refresh').prop('disabled', false);
            $('.Multirefresh').prop('disabled',false);
            // alert(response['status']);
            console.log(response);
          },
          error: function(error){
            console.log('U have done error')
            console.log(error);
          }
        });
      },
      error: function(error){
        console.log('U have done error')
        console.log(error);
      }
    });
    let st = setInterval(() => {
      $.ajax({
        type:'POST',
        url: '/Status',
        data : JSON.stringify({'data': weblist}),
        contentType: "application/json",
        error: function(error){
          console.log('U have done error')
          console.log(error);
        },
        success: function(response2){
          console.log('instant response '+ JSON.stringify(response2.status))
          var status_variable = JSON.stringify(response2.status)
          console.log(JSON.parse(status_variable))
        },
      });
    }, 1000);
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
  $('.reset').on('click', function(){
    window.location.replace('/resetstatus')
  })
</script>
</body>
</html>

