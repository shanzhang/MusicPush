var list_index;
var current_url;

function activeChanger(){
  $(".active-changer").click(function(){
    $(".active-changer").removeClass('active');
    $(this).addClass('active');
    var str = $(this).text();
    var artist = str.split(' -')[0];
    var title = str.split(' -')[1];
    var index  = $(this).index() + 2;
    list_index = index;
    playMe( artist, title ,index );
  })
}

function autoPlayList(){
  var username = getUsername();
  $.ajax({
    url:'getFavList?username=' + username,
    data:'',
    success:function(data){
      var n = data.split("&Count=")[1];
      data = data.split("&Count=")[0];
      for (var i = 0; i < n; i++) {
        var tuple = data.split('&p&')[i];
        var tit = tuple.split('|')[0];
        var art = tuple.split('|')[1];
        if ( i == 0)
          $("#my-list").append("<li class='active active-changer' style='height:26px;overflow:hidden;'><a>" + tit + ' - ' + art + "</a></li>");
        else
          $("#my-list").append("<li class='active-changer' style='height:26px;overflow:hidden;'><a>" + tit + ' - ' + art + "</a></li>");
      };
    }
  }).done(function(){
    activeChanger();
    overflowDisplay();
    $("#my-list li:nth-child(2)").click();
  });
}

function overflowDisplay(){
  $(".active-changer").mouseover(function(e){
    _text=$(this).text();
      _tooltip = "<div id='tooltipdiv'><font style='font-size:16px'> "+_text+"</font></div>";
      $("body").append(_tooltip);  
      $("#tooltipdiv").show();
      $("#tooltipdiv").css({
        "top": (e.pageY + 10) + "px",
        "left":  (e.pageX - 240) + "px"
      }).show("fast");
  })
  $(".active-changer").mouseout(function(e){
    $("#tooltipdiv").remove();
  })
  $(".active-changer").mousemove(function(e){
      $("#tooltipdiv").css({
        "top": (e.pageY + 10) + "px",
        "left":  (e.pageX - 240) + "px"
      }).show();
  })
}

function playMe( arg1, arg2, arg3){
  var query = arg1 + arg2;
  if(query == "")
    alert("No query has been input!");
  else{
    resetCycle();
    var track_url;
    var artist;
    var title;
    $.ajax({
      url: "searchTrack?query=" + query,
      data:"",
      success:function(data){
        track_url = data.split('|')[0];
        artist = data.split('|')[1];
        title = data.split('|')[2];
        track_id = data.split('|')[3];
        var love_or_not;
        love_or_not = data.split('||')[1];
        if (love_or_not == '1') setLoveLight();
        else offLoveLight();  
        $("#track_id").text(track_id);
      }
    }).done(function(){
      if(track_url == 0){
        nextPlay(arg3);
        }
      else{
        playTrack(track_url ,arg3);
        $("#artist").text(artist);
        $("#title").text(title);
      }
    });
  }
}

function playTrack(data ,index){
  current_url = data;
  $("#jquery_jplayer_1").jPlayer("destroy");
  var myCirclePlayer = new CirclePlayer("#jquery_jplayer_1",
    {
      m4a:data
    },
    {
    cssSelectorAncestor: "#cp_container_1",
    canplay: function() {
      $("#jquery_jplayer_1").jPlayer("play");
    },
    ended: function(){
      nextPlay(index);
    }

  });
  clearInterval(rotation);
  rotation = setInterval("EnableRotate()",60);
}

function nextPlay(index){
  if ( cycle_or_not ){
    playTrack(current_url,index);
  }
  else{
    if(index > $("#my-list").children('li').length)
      index = 2;
    $("#my-list li:nth-child(" + index + ")").click();
    list_index = index;    
  }
}

function searchTrack(){
$("#search").click(function(){
  var query = $("#container").val();
  if(query == "")
    alert("No query has been input!");
  else{
    resetCycle();
    var track_url;
    var artist;
    var title;
    // var coverImg;
    $.ajax({
      url: "searchTrack?query=" + query,
      data:"",
      success:function(data){
        track_url = data.split('|')[0];
        artist = data.split('|')[1];
        title = data.split('|')[2];
        var love_or_not;
        love_or_not = data.split('||')[1];
        if (love_or_not == '1') setLoveLight();
        else offLoveLight();  
      }
    }).done(function(){
      if(track_url == 0)
        alert("No results for your query!")
      else{
        playTrack(track_url);
        $("#artist").text(artist);
        $("#title").text(title);
      }
    });
  }

});
}

function skipSong(){
  $("#btn-skip").click(function(){
    resetCycle();
    var track_id = getTrackId();
    var username = getUsername();
    $.ajax({
      url:'skip?track_id=' + track_id + '&username=' + username,
      data:'',
      success:function(data){
      }
    });
    nextPlay(list_index+1);
  })
}

function hateSong(){
  $("#btn-hate").click(function(){
    resetCycle();
    var track_id = getTrackId();
    var username = getUsername();   
    $.ajax({
      url:'hate?track_id=' + track_id + '&username=' + username,
      data:'',
      success:function(data){
      }
    });
    nextPlay(list_index+1);
  })
}

function loveSong(){
  $("#btn-love").click(function(){
    var track_id = getTrackId();
    var username = getUsername();
    var img_lock = 0;
    if ($(this)[0].src.indexOf('loved') < 0){
      $(this).attr('src','site_media/img/loved.png');
      img_lock = 1;
      $.ajax({
        url:'love?track_id=' + track_id + '&username=' + username,
        data:'',
        success:function(data){
        }
      });
    }
    if ($(this)[0].src.indexOf('loved') >= 0 && !img_lock){
      $(this).attr('src','site_media/img/love.png');
      $.ajax({
        url:'cancelLove?track_id=' + track_id + '&username=' + username,
        data:'',
        success:function(data){
        }
      });
    }
  })
}

function cycleSong(){
  $("#btn-cycle").click(function(){
    var track_id = getTrackId();
    var username = getUsername();
    var cycle_lock = 0;
    if(!cycle_or_not){
      $(this).attr('src','site_media/img/cycled.png');
      cycle_lock = 1;
      cycle_or_not = 1;
    }
    if(cycle_or_not && !cycle_lock){
      $(this).attr('src','site_media/img/cycle.png');
      cycle_or_not = 0;
    }
    $.ajax({
      url:'cycle?track_id=' + track_id + '&username=' + username,
      data:'',
      success:function(data){
      }
    });
  })
}

function getTrackTitle(){
    var title = $("#title").text();
    return title;
}

function getTrackId(){
    var track_id = $("#track_id").text();
    return track_id;
}

function getTrackArtist(){
    var artist = $("#artist").text();
    return artist;
}

function getUsername(){
  var username = $("#user_name").text().split(', ')[1];
  return username;
}

jQuery(document).ready(function($) {
    autoPlayList();
    searchTrack();
    skipSong();
    hateSong();
    loveSong();
    cycleSong();
});