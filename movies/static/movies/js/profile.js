
function like(movie) {

    // Get current number of likes
    var likes = movie.querySelector("#number").innerHTML

    // Increment / deincrement number of likes and change colour of button
    if (movie.classList.contains("btn-secondary")) {

       movie.className = "btn btn-danger float-left";
       likes++
       movie.querySelector("#number").innerHTML = likes

    } else {

       movie.className = "btn btn-secondary float-left";
       likes--
       movie.querySelector("#number").innerHTML = likes
    }
 }