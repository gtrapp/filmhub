
document.addEventListener('DOMContentLoaded', function () {
   const bookmark = document.querySelector('.bookmark');
   const un_bookmarked = document.querySelector('.un-bookmarked');
   const bookmarked = document.querySelector('.bookmarked');
   const remove_form = document.getElementById("remove-form");
   const add_form = document.getElementById("add-form");
   const commentForm = document.getElementById("comment-form");
   const likeButton = document.getElementById("like-button");
   const testButton = document.getElementById("testbutton");


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
         event.preventDefault();  // Prevent default form submission
         window.scrollTo({
            top: document.body.scrollHeight,
            behavior: 'smooth'  // Smooth scrolling
         });
         // Optionally add a slight delay before submitting to allow the scroll to finish
         setTimeout(function () {
            commentForm.submit();  // Submit the form after scroll
         }, 300);  // Adjust the delay based on the scroll duration
      }
   });



   likeButton.addEventListener("click", function () {
      const heart = likeButton;
      likeButton.classList.toggle("btn-red-heart");
   });




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


   testButton.addEventListener("click", function (event) {
      testHandler();
   });

   function testHandler() {
      console.log("test handler");
   }


});

