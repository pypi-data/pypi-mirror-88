Array.from(document.getElementsByClassName("expander")).map(element => {
  element.addEventListener("click", function() {
    let target_id = this.getAttribute('expand_target');
    let target = document.getElementById(target_id);
    target.style.display = target.style.display === "block" ? "none" : "block";
  });
})
