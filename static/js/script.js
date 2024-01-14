document.addEventListener('DOMContentLoaded', () => {
    const Navigation = (() => {
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
            setupSearch: _setupSearch
        };
    })();

    Navigation.setupSearch();
});