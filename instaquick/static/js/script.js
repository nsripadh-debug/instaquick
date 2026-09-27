function toggleProfileMenu() {
    const menu = document.getElementById("profileMenu");
    menu.classList.toggle("show");
}

// close the dropdown when clicking anywhere else on the page
document.addEventListener("click", function (e) {
    const dropdown = document.querySelector(".profile-dropdown");
    if (dropdown && !dropdown.contains(e.target)) {
        document.getElementById("profileMenu")?.classList.remove("show");
    }
});
