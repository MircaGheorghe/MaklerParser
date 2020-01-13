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
  $( document ).ready(function() {
    $('.trigger3').on('click', function() {
       $('.modal-wrapper3').toggleClass('open');
      $('.page-wrapper3').toggleClass('blur-it');
       return false;
    });
  });

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

//trimiterea datelor din forma de adaugare a categoriei/reinnoirea tabelului
  $("#category_add_form").on("submit", function (e) {
      e.preventDefault();
    content = $("#category_input").val();
    name = $("#category_name_input").val();
    $.ajax({
      url: '/set_category',
      data: {
          "name" : name,
          "rez" : content
      },
      success: function (data) {
          $('#render_table').html(data)
      }
    });
  });

//trimiterea datelor din forma de adaugare a contului
  $("#cont_add_form").on("submit", function (e) {
    e.preventDefault();
  login = $("#cont_login").val();
  pass = $("#cont_pass").val();
  author = $("#cont_author").val();
  $.ajax({
    url: '/set_account',
    data: {
        "login" : login,
        "pass" : pass,
        "author" : author
    },
    success: function (data) {
      $('modal-wrapper3').html(data)
    }
  });
});

//trimiterea datelor din forma de adaugare a link-ului
$("#link_add_form").on("submit", function (e) {
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
      $('#render_table').html(data)
    }
  });
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
    $('#render_table').html(data)
  }
});
});