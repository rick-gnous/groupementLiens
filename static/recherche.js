function recherche() {
  let categorie = document.getElementById("categorie").value;
  let listElem = document.getElementsByClassName("elem");
  if (categorie == "tout") {
    for (let element of listElem) {
      element.classList.remove("hide");
    }
  } else {
    for (let element of listElem) {
      if (element.classList.contains(categorie)) {
        element.classList.remove("hide");
      } else {
        element.classList.add("hide");
      }
    }
  }
}
