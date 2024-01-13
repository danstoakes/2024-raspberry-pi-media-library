document.addEventListener('DOMContentLoaded', () => {
    const Navigation = (() => {
        function _setupHamburger() {
            const hamburger = document.querySelector(".hamburger-menu");
            const navUL = document.querySelector("nav ul");
        
            hamburger.addEventListener("click", function() {
                navUL.classList.toggle("active");
            });
        }

        return {
            setupHamburger: _setupHamburger
        };
    })();

    Navigation.setupHamburger();
});