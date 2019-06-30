function makeCookie(cname, cvalue, chours){
  var d = new Date();
  d.setTime(d.getTime() + (chours*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  document.cookie = cname+"="+cvalue+";"+ expires + ";path=/";
  console.log("Made a cookie: " + cname + " = " + cvalue);
}

function getCookie(cn){  //function inspired from https://stackoverflow.com/questions/10730362/get-cookie-by-name
  var cookies = "; " + document.cookie;
  var car = cookies.split("; " + cn + "=");
  if(car.length == 2){
    return car.pop().split(";").shift();
  }
}
