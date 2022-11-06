const updateScheme = e => {
    var giscus = document.querySelector(".giscus-frame");
    var a = localStorage.getItem('data-md-color-scheme');
    var theme = a === "slate" ? "dark" : "light";
    giscus.contentWindow.postMessage(
        { giscus: { setConfig: { theme } } },
        "https://giscus.app"
    )
}

window.addEventListener('load', updateScheme, false);

(() => {
    var p = localStorage.getItem("data-md-color-primary");
    if (p) {
        document.body.setAttribute('data-md-color-primary', p);
    }
    var a = localStorage.getItem('data-md-color-scheme');
    if (a) {
        document.body.setAttribute('data-md-color-scheme', a);
    }
})()