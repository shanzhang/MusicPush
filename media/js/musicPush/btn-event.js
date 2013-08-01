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
		autoPlay();
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
		autoPlay();
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
    skipSong();
    hateSong();
    loveSong();
    cycleSong();
});