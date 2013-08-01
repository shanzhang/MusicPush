var degree = 0;
var love_btn_degree = 0;
var rotation;
var reverse_or_not = 0;
var speed = 1.0;

function EnableRotate(){
	degree = degree + 1;
	degree = degree >= 360 ? degree - 360:degree;
	if(!reverse_or_not){
		if(love_btn_degree < 180 && love_btn_degree >=0){
			love_btn_degree += speed;
			speed += 0.1;
		}
		if(love_btn_degree >= 180 && love_btn_degree < 360){
			love_btn_degree +=speed
			speed -= 0.1;
		}
		if(love_btn_degree >= 360){
			reverse_or_not = 1;
			love_btn_degree = 360;
		}
	}else{
		if(love_btn_degree < 180 && love_btn_degree >=0){
			love_btn_degree -= speed;
			speed -= 0.1;
		}
		if(love_btn_degree >= 180 && love_btn_degree <= 360){
			love_btn_degree -=speed
			speed += 0.1;
		}
		if(love_btn_degree < 0){
			reverse_or_not = 0;
			love_btn_degree = 0;
		}
	}
	$(".rotate:gt(0)").rotate(degree);
	$(".rotate:eq(0)").rotate(love_btn_degree);
	$(".prototype-wrapper").rotate(degree);
}