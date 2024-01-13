document.addEventListener('DOMContentLoaded', () => {
    const Navigation = (() => {
        function _setupHamburger () {
            const hamburger = document.querySelector(".hamburger-menu");
            const navUL = document.querySelector("nav ul");
        
            hamburger.addEventListener("click", () => {
                navUL.classList.toggle("active");
            });
        }

        function _setupSearch () {
            const searchButton = document.querySelector("nav ul .search-icon");

            searchButton.addEventListener("click", () => {
                const dropdownNav = document.querySelector(".nav-dropdown");
                const mainNav = document.querySelector("nav");

                dropdownNav.classList.toggle("nav-dropdown-hidden");
                mainNav.classList.toggle("dropdown-extended");
            });
        }

        return {
            setupHamburger: _setupHamburger,
            setupSearch: _setupSearch
        };
    })();

    Navigation.setupHamburger();
    Navigation.setupSearch();
});