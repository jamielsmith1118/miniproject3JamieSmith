let signupForm = document.getElementById("post");

signupForm.addEventListener("submit", function(e) {
   let pwd = document.getElementById("pwd").value;
   let feedback = document.getElementById("feedback");

   e.preventDefault();

   let regex1 = /[A-Z]/;
   let regex2 = /\d/;
   let regex3 = /[!\$#%]/ ;

   if (pwd.length < 8) {
      feedback.textContent = "Your password must have at least 8 characters.";
   } else if (regex1.test(pwd) === false) {
      feedback.textContent = "Your password must include an uppercase letter.";
   } else if (regex2.test(pwd) === false) {
      feedback.textContent = "Your password must include number.";
   } else if (regex3.test(pwd) === false) {
      feedback.textContent = "Your password must include one of the following: !$#%.";
   } else {
      signupForm.submit();
   }
}
);