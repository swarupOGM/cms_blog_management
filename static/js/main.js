

// SUB-MENU START

$(document).ready(function () {
  $('.closebtn').click(function () {
    $('body').removeClass('active');
    $(".wrapper").addClass("show");
  });


  $('.sidetogglebtn').on('click', function (e) {

    if ($(window).width() > 991) {
      $('body').addClass('');
    } else {
      $('body').addClass('active');
    }
    e.stopPropagation();
  });





  $('.profile__dropdown a').on('click', function (e) {
    e.stopPropagation();
  });



  $('.bell a').on('click', function (e) {
    e.stopPropagation();
  });





  $(function () {


    $(function () {
      $(".sidetogglebtn").on("click", function (e) {
        $(".nav").toggleClass("show");
      });
      $(document).on("click", function (e) {
        if ($(e.target).is(".nav, .sidetogglebtn") === false) {
          $(".nav").removeClass("show");
          $('body').removeClass('active');
        }
      });
    });



    $(".bell a").on("click", function (e) {

      $(".notification_drop").toggleClass("open");
    });
    $(document).on("click", function (e) {

      if ($(e.target).is(".notification_drop, .notification_drop ul li, .rightnoteinfo, .rightnoteinfo h3, .rightnoteinfo p, .rightnoteinfo small") === false) {
        $(".notification_drop").removeClass("open");
        // $('body').removeClass('active');
      }
    });





    $(".profile__dropdown a").on("click", function (e) {

      $(".listingMenu").toggleClass("open");
    });

  });

  $(".arrow").on("click", function (e) {
    $(".arrow").toggleClass("open");
    $(".driveronboardprt").slideToggle("slow");
  });


  $(".mob_sidetogglebtn").on("click", function (e) {
    $(".shortmenu").slideToggle("slow");


  });


  $(".set > a").on("click", function () {
    if ($(this).hasClass("active")) {
      $(this).removeClass("active");
      $(this)
        .siblings(".content")
        .slideUp(200);
      $(".set > a i")
        .removeClass("fa-angle-up")
        .addClass("fa-angle-down");
    } else {
      $(".set > a i")
        .removeClass("fa-angle-up")
        .addClass("fa-angle-down");
      $(this)
        .find("i")
        .removeClass("fa-angle-down")
        .addClass("fa-angle-up");
      $(".set > a").removeClass("active");
      $(this).addClass("active");
      $(".content").slideUp(200);
      $(this)
        .siblings(".content")
        .slideDown(200);
    }
  });

});

// $(".profile__dropdown a").click(function () {
//   $(".listingMenu").toggleClass("open");

// });




$('.online_mood input[type="checkbox"]').on('change', function (e) {
  if (e.target) {
    $('.offline-mood').addClass('model-open');
    $(".online").css("display", "none");
    $(".offline").css("display", "inline-block");
  }
  if (e.target.checked) {
    $('.offline-mood').removeClass('model-open');
    $(".offline").css("display", "none");
    $(".online").css("display", "inline-block");
  }
});


$(".accept-toggle").on('click', function () {
  $(".changepassword").addClass('model-open');
});

$(".verify").on('click', function () {
  $(".inputPassword").addClass('model-open');
});

$(".reject").on('click', function () {
  $(".rejectpop").addClass('model-open');
});

$(".closemodal, .bg-overlay").click(function () {
  $(".offline-mood").removeClass('model-open');
  $(".changepassword").removeClass('model-open');
  $(".inputPassword").removeClass('model-open');
  $(".rejectpop").removeClass('model-open');
});



$(".toggle-password").click(function () {

  $(this).toggleClass("fa-eye fa-eye-slash");
  var input = $($(this).attr("toggle"));
  if (input.attr("type") == "password") {
    input.attr("type", "text");
  } else {
    input.attr("type", "password");
  }
});



$('.faq__close').click(function () {
  let id = $(this).data('id');
  $('.open' + id).css("display", "none");
});


$('.counter').each(function () {
  $(this).prop('Counter', 0).animate({
    Counter: $(this).text()
  }, {
    duration: 2000,
    easing: 'swing',
    step: function (now) {
      $(this).text(Math.ceil(now));
    }
  });
});







































