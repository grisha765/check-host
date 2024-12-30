document.addEventListener("DOMContentLoaded", () => {
    const copyButtons = document.querySelectorAll(".copy-btn");

    copyButtons.forEach(button => {
        button.addEventListener("click", () => {
            const targetId = button.getAttribute("data-target");
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                const textToCopy = targetElement.textContent;

                if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(textToCopy)
                        .then(() => {
                            showCopySuccess(button);
                        })
                        .catch(err => {
                            console.error("Failed to copy using Clipboard API:", err);
                            fallbackCopyToClipboard(textToCopy, button);
                        });
                } else {
                    fallbackCopyToClipboard(textToCopy, button);
                }
            }
        });
    });

    function showCopySuccess(button) {
        button.textContent = "Copied!";
        setTimeout(() => button.textContent = "Copy", 2000);
    }

    function fallbackCopyToClipboard(text, button) {
        const textarea = document.createElement("textarea");
        textarea.value = text;
        textarea.style.position = "fixed";
        document.body.appendChild(textarea);
        textarea.focus();
        textarea.select();

        try {
            const successful = document.execCommand("copy");
            if (successful) {
                showCopySuccess(button);
            } else {
                console.error("Fallback: Copy command was unsuccessful");
                button.textContent = "Error!";
                setTimeout(() => button.textContent = "Copy", 2000);
            }
        } catch (err) {
            console.error("Fallback: Unable to copy", err);
            button.textContent = "Error!";
            setTimeout(() => button.textContent = "Copy", 2000);
        }

        document.body.removeChild(textarea);
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const ipAddressElement = document.getElementById("ip-address");

    if (ipAddressElement) {
        ipAddressElement.addEventListener("click", () => {
            const ipText = ipAddressElement.textContent;

            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(ipText)
                    .then(() => {
                        showNotification("IP address copied!");
                    })
                    .catch(err => {
                        console.error("Failed to copy IP address:", err);
                        fallbackCopyToClipboard(ipText, "IP address copied!");
                    });
            } else {
                fallbackCopyToClipboard(ipText, "IP address copied!");
            }
        });
    }

    function showNotification(message) {
        const notification = document.createElement("div");
        notification.className = "notification";
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.add("fade-out");
            notification.addEventListener("transitionend", () => {
                document.body.removeChild(notification);
            });
        }, 2000);
    }

    function fallbackCopyToClipboard(text, message) {
        const textarea = document.createElement("textarea");
        textarea.value = text;
        textarea.style.position = "fixed";
        document.body.appendChild(textarea);
        textarea.focus();
        textarea.select();

        try {
            const successful = document.execCommand("copy");
            if (successful) {
                showNotification(message);
            } else {
                console.error("Fallback: Copy command was unsuccessful");
                showNotification("Failed to copy IP address!");
            }
        } catch (err) {
            console.error("Fallback: Unable to copy", err);
            showNotification("Failed to copy IP address!");
        }

        document.body.removeChild(textarea);
    }
});

