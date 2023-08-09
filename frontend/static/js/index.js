function changeClass1(value) {  
  var string="SC/ST";
  if(value === string )
  {
  document.getElementsByClassName("sc")[0].style.display="block";
  alert("Since you category is "+value+" ,you should enter your category rank only")
  }
  else{

  }

  var string="OBC";
  if(value === string )
  {
  document.getElementsByClassName("sc")[0].style.display="block";
  alert("Since you category is "+value+" ,you should enter your category rank only")
  }
  else{

  }

  var string="PWD";
  if(value === string )
  {
  document.getElementsByClassName("sc")[0].style.display="block";
  alert("Since you category is "+value+" ,you should enter your category rank only")
  }
  else{

  }

}

// college overview
function cutoff()
{
  document.getElementsByClassName("ow2")[0].style.display="block";
  document.getElementsByClassName("ow")[0].style.display="none";
}
function ovw()
{
  document.getElementsByClassName("ow2")[0].style.display="none";
  document.getElementsByClassName("ow")[0].style.display="block";
}
