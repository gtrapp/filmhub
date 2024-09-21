document.addEventListener('DOMContentLoaded', function () {
    const bookmark = document.querySelector('.bookmark');
    const un_bookmarked = document.querySelector('.un-bookmarked');
    const bookmarked = document.querySelector('.bookmarked');
    const remove_form = document.getElementById("remove-form");
    const add_form = document.getElementById("add-form");
    const commentForm = document.getElementById("comment-form");
    const likeButton = document.getElementById("like-button");

    if (un_bookmarked != null) {
       console.log("un_bookmarked exists");
       un_bookmarked.addEventListener("click", () => {
          console.log("un_bookmarked clicked");
          add_form.submit();
       })
    } else if (bookmarked != null) {
       console.log("bookmarked exists");
       bookmarked.addEventListener("click", () => {
          console.log("un_bookmarked clicked");
          remove_form.submit();
       })
    } else {
       console.log("bookmark exists");
    }

    commentForm.addEventListener("keypress", function (event) {
       // Check if the keyCode for "Enter" (13) was pressed
       if (event.keyCode === 13) {
          event.preventDefault();  // Prevent the default form submission if needed
          commentForm.submit();  // Submit the form
       }
       window.scrollTo({
          top: document.body.scrollHeight,
          behavior: 'smooth' // Smooth scrolling
       });
    });

    likeButton.addEventListener("click", function () {
       const heart = likeButton;
       likeButton.classList.toggle("btn-red-heart");
    });
    




    // // Store the scroll position on unload
    // window.addEventListener('beforeunload', function () {
    //    localStorage.setItem('scrollPosition', window.scrollY);
    // });

    // // Restore the scroll position on load
    // window.addEventListener('load', function () {
    //    if (localStorage.getItem('scrollPosition')) {
    //       window.scrollTo(0, localStorage.getItem('scrollPosition'));
    //       localStorage.removeItem('scrollPosition');
    //    }
    // });


    window.addEventListener("beforeunload", function () {
       localStorage.setItem("scrollPosition", window.scrollY);
    });

    // Restore the scroll position after the page is loaded
    window.addEventListener("load", function () {
       const scrollPosition = localStorage.getItem("scrollPosition");
       if (scrollPosition !== null) {
          window.scrollTo(0, parseInt(scrollPosition));
       }
    });



 });


 // function like(post) {
 //    // Get current number of likes
 //    var likes = post.querySelector("#number").innerHTML

 //    // Increment / deincrement number of likes and change colour of button
 //    if (post.classList.contains("btn-secondary")) {

 //       post.className = "btn btn-danger float-left";
 //       likes++
 //       post.querySelector("#number").innerHTML = likes

 //    } else {

 //       post.className = "btn btn-secondary float-left";
 //       likes--
 //       post.querySelector("#number").innerHTML = likes
 //    }
 // }