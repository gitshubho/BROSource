 $(document).ready(function()
{
      /* Setting the Animation Of the home Page*/
      var Wht=$(window).height();
      var Wwt=$(window).width();



        $(".onboarding-append-work").click(function()
        {
          $(".onboarding-work").append("<div class='form-group'>\
            <div class='row'>\
              <div class='col-md-9 col-xs-9'>\
                <label>Service</label>\
                <input type='text' class='form-control' name = 'work' placeholder='ex: Create a minimal and responsive website'>\
              </div>\
              <div class='col-md-3 col-xs-3'>\
                <label>Price (USD)</label>\
                <input type='text' class='form-control' name = 'workprice' placeholder='ex: 5'>\
              </div>\
            </div>\
          </div>");
        });

      $(".homepage-add-projects-button").css("top",Wht);
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
      $('.onboarding-carousel').each(function()
      {
        $(this).carousel(
        {
          interval: false
        });
      });

    $(".homepage-carousel").css("top",Wht/4.5);

    $(".cards").css("top",Wht/10);
    $(".footer").css("height",Wht/3);
    $(".profile-other-user").css("height",Wht/10);

    var Onboarding_navHt=$("#onboarding-nav").height()
    $(".onboarding-carousel-control").css("top",Onboarding_navHt/2);
    $(".onboarding-carousel-control").css("font-size",Onboarding_navHt*3.2+"%");
         /*Seting the grid-card size */
  if(Wwt>Wht)
    {
      $(".homepage-image-active-carousel-image").css("height",Wht/1.64);
      if(Wht>1000)
      {
        var card_height=Wht/6;
        $(".customcard").css("height",card_height);
        $(".homepage-add-projects-button").css("margin-top","15%");
        $(".cards").css("top",Wht/6);

        if(Wwt<1430 && Wwt>1000)
        {
          var card_height=Wht/5;
          $(".customcard").css("height",card_height);
          $(".footer").css("height",Wht/2.5);
        }
        else if(Wwt<1700 && Wwt>1400)
        {
          var card_height=Wht/5.5;
          $(".customcard").css("height",card_height);
        }
      }
      else
      {
        var card_height=Wht/3;
        $(".customcard").css("height",card_height);
        $(".footer").css("height",Wht/2.5);
      }
      if(Wwt>2000)
      {
        var card_height=Wht/5;
        $(".customcard").css("height",card_height);
      }
    }
      else
      {
        $(".homepage-image-active-carousel-image").css("height",Wht/2.5);
        $(".homepage-image-active-carousel-image").css("width",Wwt);
        $(".footer").css("height",Wht/2.2);
        $(".homepage-add-projects-button").css("margin-top","50%");
        $(".cards").css("top",Wht/5);
        $(".homepage-carousel").css("top",Wht/3);
        if(Wwt>700)
        {
          var card_height=Wht/6;
          $(".customcard").css("height",card_height);
        }
        else if(Wwt>413)
        {
          var card_height=Wht/3.4;
          $(".customcard").css("height",card_height);
        }
        else if(Wwt>330)
        {
          var card_height=Wht/3;
          $(".customcard").css("height",card_height);
        }
        else if(Wwt<330)
        {
          var card_height=Wht/3;
          $(".customcard").css("height",card_height);
        }
        else
        {
          var card_height=Wht/3.6;
          $(".customcard").css("height",card_height);
        }
      }
       $(".card-footer").css("top",card_height-50);
      /*Fixing the profile or profile_other*/

        var fix_profile_bottom=$(".fix-profile").bottom;
      if(Wwt<800 && fix_profile_bottom<Wht)
      {
        $(".fix-profile").removeClass("affix");
      }
      else
      {
          $(".fix-profile").removeClass("affix");
      }

      /* */


      /* */

      /*Modal JS, The Signup/Login Toggle Effect*/
      $(".Signup").hide();
      $(".modal-header-button").on("click",function()
      {
        $(".modal-header-button").toggleClass("selected");
        $(".modal-header-button").toggleClass("deselected");
        $(".modal-footer").toggleClass("borderless");
        $(".modal-footer").toggleClass("bordered");
      });
      $("#modal-login-holder").on("click",function()
      {
        $(".Login").show();
        $(".Signup").hide();
      });
      $("#modal-signup-holder").on("click",function()
      {
        $(".Signup").show('fast');
        $(".Login").hide();
      });
      $(".modal-body").bind("scroll", function()
      {
        var modal_Body_Height = $(".modal-body").height();
         if ($(".modal-body").scrollTop()>modal_Body_Height/5)
         {
           $("#modal-scroll-icon").removeClass("glyphicon-menu-down");
           $("#modal-scroll-icon").addClass("glyphicon-menu-up");
         }
         else
         {
           $("#modal-scroll-icon").removeClass("glyphicon-menu-up");
           $("#modal-scroll-icon").addClass("glyphicon-menu-down");     }
      });
    /*Profile Page-Self Begins*/
    /**/
    /**/
    /**/
    /**/

    $(".profile-self-info-footer-tab").on("click",function()
    {

        $(".profile-self-info-footer-tab").addClass("topborder-invisible");
        $(".profile-self-info-footer-tab").removeClass("topborder-visible");
        $(this).toggleClass("topborder-invisible");
        $(this).toggleClass("topborder-visible");
    });
    var NavHtOnboard=$("#onboarding-nav").height();
      $("#onboarding-carousel-indicators div").css("height",NavHtOnboard/2);
      $("#onboarding-carousel-indicators div").css("width",NavHtOnboard/2);
      $("#onboarding-carousel-indicators span").css("font-size",NavHtOnboard/4);

     var NavHt=$(".navbar").height();
      $(".bar").css("padding-top",NavHt);


      /**//**//*Onboarding*/

});

$(window).resize(function()
{
    var Wht=$(window).height();
    var Wwt=$(window).width();
      $(".cards").css("top",Wht/2.2);
    var NavHt=$("#onboarding-nav").height();
    $("#onboarding-carousel-indicators div").css("height",NavHt/2);
    $("#onboarding-carousel-indicators div").css("width",NavHt/2);
    $("#onboarding-carousel-indicators span").css("font-size",NavHt/4);

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
    $(".homepage-carousel").css("top",Wht/4.5);
    $(".homepage-add-projects-button").css("margin-top","10%");
    $(".cards").css("top",Wht/10);
    $(".footer").css("height",Wht/3);

    var Onboarding_navHt=$("#onboarding-nav").height()
    $(".onboarding-carousel-control").css("top",Onboarding_navHt/2);
    $(".onboarding-carousel-control").css("font-size",Onboarding_navHt*3.2+"%");

    if(Wwt>Wht)
    {
      $(".homepage-image-active-carousel-image").css("height",Wht/1.64);
      if(Wht>1000)
      {
        var card_height=Wht/6;
        $(".customcard").css("height",card_height);
        $(".homepage-add-projects-button").css("margin-top","15%");
        $(".cards").css("top",Wht/6);
        $(".profile-other-user").css("height",Wht/8);
        if(Wwt<1430 && Wwt>1000)
        {
          var card_height=Wht/5;
          $(".customcard").css("height",card_height);
          $(".footer").css("height",Wht/2.5);
        }
        else if(Wwt<1700 && Wwt>1400)
        {
          var card_height=Wht/5.5;
          $(".customcard").css("height",card_height);
        }
      }
      else
      {
        var card_height=Wht/3;
        $(".customcard").css("height",card_height);
        $(".footer").css("height",Wht/2.5);
      }
      if(Wwt>2000)
      {
        var card_height=Wht/5;
        $(".customcard").css("height",card_height);
      }

    }
      else
      {
        $(".homepage-image-active-carousel-image").css("height",Wht/2.5);
        $(".homepage-image-active-carousel-image").css("width",Wwt);
        $(".footer").css("height",Wht/2.2);
        $(".homepage-add-projects-button").css("margin-top","50%");
        $(".cards").css("top",Wht/5);
        $(".homepage-carousel").css("top",Wht/3);
        if(Wwt>700)
        {
          var card_height=Wht/6;
          $(".customcard").css("height",card_height);
        }
        else if(Wwt>413)
        {
          var card_height=Wht/3.4;
          $(".customcard").css("height",card_height);
        }
        else if(Wwt>330)
        {
          var card_height=Wht/3;
          $(".customcard").css("height",card_height);
        }
        else if(Wwt<330)
        {
          var card_height=Wht/3;
          $(".customcard").css("height",card_height);
        }
        else
        {
          var card_height=Wht/3.6;
          $(".customcard").css("height",card_height);
        }
      }

      $(".card-footer").css("top",card_height-50);
      /*Fixing the profile or profile_other*/

      if(Wwt<800)
      {
        $(".fix-profile").removeClass("affix");
      }
      else
      {
          $(".fix-profile").addClass("affix");
      }

      /* */

      var NavHt=$(".navbar").height();
      $(".content").css("top",NavHt+20)
});
