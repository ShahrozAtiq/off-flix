window.addEventListener("keydown", function(event) {
    if (event.keyCode == 116) {
        // block F5 (Refresh)
        event.preventDefault();
        event.stopPropagation();
        return false;

    } else if (event.keyCode == 122) {
        // block F11 (Fullscreen)
        event.preventDefault();
        event.stopPropagation();
        return false;

    } else if (event.keyCode == 123) {
        // block F12 (DevTools)
        event.preventDefault();
        event.stopPropagation();
        return false;

    } else if (event.ctrlKey && event.shiftKey && event.keyCode == 73) {
        // block Strg+Shift+I (DevTools)
        event.preventDefault();
        event.stopPropagation();
        return false;

    } else if (event.ctrlKey && event.shiftKey && event.keyCode == 74) {
        // block Strg+Shift+J (Console)
        event.preventDefault();
        event.stopPropagation();
        return false;
    }
});
window.oncontextmenu = function(event) {
    // block right-click / context-menu
    event.preventDefault();
    event.stopPropagation();
    return false;
};