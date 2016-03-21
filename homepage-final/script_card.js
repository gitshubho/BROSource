$(document).ready(function()
{
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
        $(".card-footer").css("height",card_header_ht);
        $(".customcard").css("font-size",card_height/2.1+"%");
      }
      else
      {
        var card_height=Wht/2.6;
        var card_header_ht=$(".card-header").height();
        $(".customcard").css("height",card_height);
        var card_body_ht=$(".customcard").height()/1.85;
        $(".card-body").css("height",card_body_ht);
        $(".card-footer").css("height",card_header_ht);
        $(".customcard").css("font-size",card_height/2.3+"%");
      }
});
