$(document).ready(function()
{
      /* Setting the Animation Of the home Page*/
      var Wht=$(window).height();
      var Wwt=$(window).width();
      if(Wht<Wwt)
      {
        $(".hello-image-center").css("height",Wht*1.1/3);
        $(".hello-image-out").css("height",Wht*1/3);
        $(".hello-image-outermost").css("height",Wht*0.9/3);
      }
      else
      {
        $(".hello-image-center").css("height",Wht*0.9/3);
        $(".hello-image-out").css("height",Wht*0.8/3);
        $(".hello-image-outermost").css("height",Wht*0.6/3);

      }
      $(".hello-image-left").addClass("animated fadeInRight");
      $(".hello-image-right").addClass("animated fadeInLeft");
      $('.carousel').each(function()
      {
        $(this).carousel(
        {
          interval: false
        });
      });

    /* Navbar-Animation effect*/
      $(window).bind("scroll", function() {
      var navHeight = $( window ).height();
         if ($(window).scrollTop()>navHeight/1.4) {
            $('.search').addClass('search-on-scroll');
            $('.initial-search').addClass('invisible');
            $('.navbar-container').addClass('nav-fixed');
            $('.search').removeClass('animated fadeOut');

         }
         else{
            $('.search').removeClass('search-on-scroll');
            $('.initial-search').removeClass('invisible');
            $('.navbar-container').removeClass('nav-fixed');
            $('.search').addClass('animated fadeOut')
         }
         });

         /*Seting the grid-card size */
      var Wht=$(window).height();
      var Wwt=$(window).width();
      if(Wwt>Wht && Wwt>1000)
      {
        var card_height=Wht/3.6;
        var card_header_ht=$(".card-header").height();
        $(".customcard").css("height",card_height);
        var card_body_ht=$(".customcard").height()/1.75;
        $(".card-body").css("height",card_body_ht);
        var card_footer_ht=$(".card-footer").height();
      }
      else
      {
        var card_height=Wht/2.6;
        var card_header_ht=$(".card-header").height();
        $(".customcard").css("height",card_height);
        var card_body_ht=$(".customcard").height()/1.85;
        $(".card-body").css("height",card_body_ht);
      }

      /*Creating the Animation For the Card Flip*/
      $(".customcard").children(".card-front").addClass("visible");
      $(".customcard").children(".card-flip").addClass("invisible");
      $(".customcard").click(function()
      {
        $(this).addClass("animated flipOutY");
        setTimeout(animate,600,$(this));
      });

      function animate(thisObj)
      {
        thisObj.removeClass("animated flipOutY");
        if(thisObj.children(".card-front").hasClass("visible"))
        {
        thisObj.children(".card-front").removeClass("visible");
        thisObj.children(".card-front").addClass("invisible");
        thisObj.children(".card-flip").removeClass("invisible");
        thisObj.children(".card-flip").addClass("visible");
        }
        else
        {
          thisObj.children(".card-front").removeClass("invisible");
          thisObj.children(".card-front").addClass("visible");
          thisObj.children(".card-flip").removeClass("visible");
          thisObj.children(".card-flip").addClass("invisible");
        }
      }

});
