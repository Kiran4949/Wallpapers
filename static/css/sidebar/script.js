let arrow = document.querySelectorAll(".arrow");
let categoryLinks = document.querySelectorAll(".category-link");

// Function to toggle the dropdown menu
function toggleMenu(e) {
  let arrowParent = e.target.closest("li");
  arrowParent.classList.toggle("showMenu");
}

// Add click event listener to the chevron icon
for (var i = 0; i < arrow.length; i++) {
  arrow[i].addEventListener("click", toggleMenu);
}

// Add click event listener to the "Category" link
for (var i = 0; i < categoryLinks.length; i++) {
  categoryLinks[i].addEventListener("click", toggleMenu);
}

// Sidebar toggle functionality
let sidebar = document.querySelector(".sidebar");
let sidebarBtn = document.querySelector(".bx-menu");

sidebarBtn.addEventListener("click", () => {
  sidebar.classList.toggle("close");
});
