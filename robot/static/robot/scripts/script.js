 //AJAX REQUEST

  //schimbarea textului pe pagina principala
  $(".start_link").on("click", function () {

    $.ajax({
      url: '/change_status',
      data: {
      },
      dataType: 'json',
      success: function (data) {
        if(data.status == false){
            $(".start_link").html("Inactiv");
            $(".start_link").removeClass( "btn-success" ).addClass( "btn-danger" );
        }
        else {
            $(".start_link").html("Activ");
            $(".start_link").removeClass( "btn-danger" ).addClass( "btn-success" );
        }
      }
    });
  });

//trimiterea datelor din forma de adaugare a categoriei/reinnoirea tabelului si modalului
$(document).on("submit", "#category_add_form", function (e) {
  e.preventDefault();
  content = $("#category_link_input").val();
  name = $("#category_name_input").val();
    $.ajax({
      url: '/set_category',
      data: {
          "name" : name,
          "rez" : content
      },
      //alert datele au fost trimise cu succes
      success: function (data) {
        $('.alert').toggleClass('display_off');
        setTimeout(hide_alert, 2000);
        get_table(); get_modal();
      }
  });
  //golirea casetelor de text
  $("#category_link_input").val('');
  $("#category_name_input").val('');
});

//trimiterea datelor din forma de adaugare a contului/reinoirea modalului
  $(document).on("submit","#cont_add_form", function (e) {
    e.preventDefault();
  login = $("#cont_login").val();
  pass = $("#cont_pass").val();
  author = $("#curent_user").val();
  alert(author);
  $.ajax({
    url: '/set_account',
    data: {
        "login" : login,
        "pass" : pass,
        "author" : author
    },
    success: function (data) {
      $('.alert').toggleClass('display_off');
      setTimeout(hide_alert, 2000);
      get_modal();
    }
  });
  $('#cont_login').val('');
  $('#cont_pass').val('');
});

//trimiterea datelor din forma de adaugare a link-ului/reinoirea tabelului
$(document).on("submit", "#link_add_form", function (e) {
    e.preventDefault();
    link = $("#link_content").val();
    cont = $("#link_select_cont").val();
    category = $("#link_select_category").val();
    cu_plata = $("#link_cu_plata").is(':checked');
  $.ajax({
    url: '/set_link',
    data: {
        "link" : link,
        "cont" : cont,
        "category" : category,
        "cu_plata" : cu_plata
    },
    success: function (data) {
      $('.alert').toggleClass('display_off');
      setTimeout(hide_alert, 2000);
      get_table();
    }
  });
  $("#link_content").val('');
});



$(document).on('click', '.delete_button', function() {
  $(".yes_delete").data("id", $(this).data("id"));
});




//stergerea unui link
$(document).on("click", ".yes_delete" ,function () {
  id = $(this).data("id");
$.ajax({
  url: '/delete_link_cat',
  data: {
      "id" : id,
  },
  success: function (data) {
    get_table();
    get_modal();
  }
});
});


function get_modal(){
  $.ajax({
    url: '/get_modal',
    success: function (data) {
      $('#modal_add_link').html(data)
    }
  });
}

function get_table(){
  $.ajax({
    url: '/get_table',
    success: function (data) {
      $('.container-fluid').html(data)
    }
  });
}

function hide_alert() {
  $('.alert').addClass('display_off');
}