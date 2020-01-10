$( document ).ready(function() {
    $("#field").change(function(){
        var id = $(this).find("option:selected").attr("id");
        switch (id){
            case "acc":
            $(function(){
                $('.modal-wrapper').toggleClass('open');
                $('.page-wrapper').toggleClass('blur-it');
                return false;
            }); break;
            case "cat":
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
  console.log($(this).data("id"))
  $(".yes_delete").data("id", $(this).data("id"));
  $('.modal-delete').toggleClass('open');
      $('.page-wrapper4').toggleClass('blur-it');
       return false;
});

  //ajax requests
  $(".start_link").on("click", function () {

    $.ajax({
      url: '/start',
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


  $("#category_add_form").on("submit", function (e) {
      e.preventDefault();
    content = $("#category_input").val();
    $.ajax({
      url: '/set_category',
      data: {
          "rez" : content
      },
      success: function (data) {
          $('.modal-wrapper3').html(data)
      }
    });
  });


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
      $('#render_table').html(data)
    }
  });
});

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


$(document).on("click", ".yes_delete" ,function () {
  id = $(this).data("id");
  console.log(id)
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