document.addEventListener('DOMContentLoaded', () => {
    const Locker = (() => {
        let enteredKeys = '';
        const scriptTag = document.getElementById("LockerScript");
        const password = scriptTag.getAttribute('data-password').toLowerCase();

        function _setupPassword() {
            document.addEventListener('keydown', (event) => {
                if (event.key === 'Backspace') {
                    enteredKeys = '';
                } else {
                    enteredKeys += event.key.toLowerCase();
                    _checkPassword();
                }
            });
        }

        function _checkPassword() {
            if (enteredKeys === password) {
                document.getElementById("LockerContent").classList.remove("hidden");
                enteredKeys = '';
            }
        }

        return {
            setupPassword: _setupPassword
        };
    })();

    Locker.setupPassword();
});