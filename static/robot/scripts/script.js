$( document ).ready(function() {
    $("#what_to_add").on('click', function(){
        var id = $("#field option:selected").attr("id");
        switch (id){
            case "cat":
            $(function(){
                $('.modal-wrapper').toggleClass('open');
                $('.page-wrapper').toggleClass('blur-it');
                return false;
            }); break;
            case "acc":
            $(function(){
                $('.modal-wrapper2').toggleClass('open');
                $('.page-wrapper').toggleClass('blur-it');
                return false;
            }); break;
            case "link":
            $(function(){
                $('.modal-wrapper3').toggleClass('open');
                $('.page-wrapper').toggleClass('blur-it');
                return false;
            });
        }
    });
});


  $( document ).ready(function() {
    $('.trigger').on('click', function() {
       $('.modal-wrapper').toggleClass('open');
      $('.page-wrapper').toggleClass('blur-it');
       return false;
    });
  });
  $( document ).ready(function() {
    $('.trigger2').on('click', function() {
       $('.modal-wrapper2').toggleClass('open');
      $('.page-wrapper2').toggleClass('blur-it');
       return false;
    });
  });

  $(document).on("click", ".trigger3", function(){
    $('.modal-wrapper3').toggleClass('open');
      $('.page-wrapper3').toggleClass('blur-it');
       return false;
  })

  $( document ).ready(function() {
    $('.trigger4').on('click', function() {
       $('.modal-delete').toggleClass('open');
      $('.page-wrapper4').toggleClass('blur-it');
       return false;
    });
  });
$(document).on('click', '.delete_button', function() {
  $(".yes_delete").data("id", $(this).data("id"));
  $('.modal-delete').toggleClass('open');
      $('.page-wrapper4').toggleClass('blur-it');
       return false;
});

  //AJAX REQUEST

  //schimbarea textului pe pagina principala
  $(".start_link").on("click", function () {

    $.ajax({
      url: '/change_text',
      data: {
      },
      dataType: 'json',
      success: function (data) {
        if(data.status == false){
            $(".spec").html("dezactivat")
        }
        else {
            $(".spec").html("activat")
        }
      }
    });
  });
//pornirea parserului
  $(".start_link").on("click", function () {

    $.ajax({
      url: '/start_parser',
      data: {
      },
      dataType: 'json',
      success: function (data) {
      }
    });
  });

//trimiterea datelor din forma de adaugare a categoriei/reinnoirea tabelului si modalului
$(document).on("submit", "#category_add_form", function (e) {
  e.preventDefault();
  content = $("#category_link_input").val();
  name = $("#category_name_input").val();
    $.ajax({
      url: '/set_category_table',
      data: {
          "name" : name,
          "rez" : content
      },
      success: function (data) {
          get_table();
          get_modal();
      }
  });

  $("#category_link_input").val('');
  $("#category_name_input").val('');
});

//trimiterea datelor din forma de adaugare a contului
  $(document).on("submit","#cont_add_form", function (e) {
    e.preventDefault();
  login = $("#cont_login").val();
  pass = $("#cont_pass").val();
  author = $("#curent_user").val();
  $.ajax({
    url: '/set_account',
    data: {
        "login" : login,
        "pass" : pass,
        "author" : author
    },
    success: function (data) {
      get_modal();
    }
  });
  $('#cont_login').val('');
  $('#cont_pass').val('');
});

//trimiterea datelor din forma de adaugare a link-ului
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
      get_table();
    }
  });
  $("#link_content").val('');
});

//stergerea unui link
$(document).on("click", ".yes_delete" ,function () {
  id = $(this).data("id");
$.ajax({
  url: '/delete_link',
  data: {
      "id" : id,
  },
  success: function (data) {
    get_table();
  }
});
});


function get_modal(){
  $.ajax({
    url: '/get_modal',
    success: function (data) {
      $('.link_modal_form').html(data)
    }
  });
}

function get_table(){
  $.ajax({
    url: '/get_table',
    success: function (data) {
      $('#render_table').html(data)
    }
  });
}