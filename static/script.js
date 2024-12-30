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

