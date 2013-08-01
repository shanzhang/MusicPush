var cycle_or_not = 0;

function skipHover(){
	$("#btn-skip").mouseover(function(){
		$(this).attr('src','site_media/img/hskip.png');
	});
	$("#btn-skip").mouseout(function(){
		$(this).attr('src','site_media/img/skip.png');
	});
}

function hateHover(){
	$("#btn-hate").mouseover(function(){
		$(this).attr('src','site_media/img/hhate.png');
	});
	$("#btn-hate").mouseout(function(){
		$(this).attr('src','site_media/img/hate.png');
	});
}

function loveHover(){
	$("#btn-love").mouseover(function(){
		if ($(this)[0].src.indexOf('loved') < 0)
			$(this).attr('src','site_media/img/hlove.png');
	});
	$("#btn-love").mouseout(function(){
		if ($(this)[0].src.indexOf('loved') < 0)
			$(this).attr('src','site_media/img/love.png');
	});
}

function setLoveLight(){
	$("#btn-love").attr('src','site_media/img/loved.png');
}

function offLoveLight(){
	$("#btn-love").attr('src','site_media/img/love.png');	
}

function cycleHover(){
	$("#btn-cycle").mouseover(function(){
		if (!cycle_or_not)
			$(this).attr('src','site_media/img/hcycle.png');
	});
	$("#btn-cycle").mouseout(function(){
		if (!cycle_or_not)
			$(this).attr('src','site_media/img/cycle.png');
	});
}

function resetCycle(){
	cycle_or_not = 0;
	$("#btn-cycle").attr('src','site_media/img/cycle.png');
}

function exitHover(){
	$("#exit").mouseover(function(){
		$(this).attr('src','site_media/img/hlogout.png');
	});
	$("#exit").mouseout(function(){
		$(this).attr('src','site_media/img/logout.png');
	});
}

jQuery(document).ready(function($) {
	cycleHover();
	skipHover();
	loveHover();
	hateHover();
	exitHover();
});