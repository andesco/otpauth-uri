matchMedia("(min-width: 960px)").addEventListener("change",e=>{
  if(e.matches) bootstrap.Offcanvas.getInstance(document.getElementById("tocMenu"))?.hide();
});
document.getElementById("tocMenu").addEventListener("click",e=>{
  if(e.target.closest("nav a")) bootstrap.Offcanvas.getInstance(e.currentTarget).hide();
});
