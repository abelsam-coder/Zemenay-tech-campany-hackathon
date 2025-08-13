let a = navigator.platform;
        document.getElementById('device').value = a;
        console.log(a);
        document.querySelector('.messag').addEventListener("animationend",function (){
    this.style.display = "none"
})
document.querySelector("button").addEventListener("animationend",function () {
    this.style.display = "none"
})
function but() {

  // Show elements immediately
  document.querySelector('.anime').style.display = "block";
  document.querySelector('.bb').style.display = "block";

  // Redirect after 5 seconds
  setTimeout(() => {
    document.querySelector('.anime').style.display = "none";
  document.querySelector('.bb').style.display = "none";
  }, 3000);
}
