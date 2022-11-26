const updateScheme = e => {
    var giscus = document.querySelector(".giscus-frame");
    var a = localStorage.getItem('data-md-color-scheme');
    var theme = a === "default" ? "light" : "dark";
    // alert(a + " -> " + theme);
    giscus.contentWindow.postMessage(
        { giscus: { setConfig: { theme } } },
        "https://giscus.app"
    )
}

window.addEventListener('load', updateScheme, false);

const updateBoxFontColor = e => {
    var a = localStorage.getItem('data-md-color-scheme');
    if (a !== "default") {
        var elements = document.getElementsByClassName('box');
        for (var i in elements) {
            // alert(elements[i].style.color);
            elements[i].style.color = "white";
        }
    }
}

(() => {
    var p = localStorage.getItem("data-md-color-primary");
    if (p) {
        document.body.setAttribute('data-md-color-primary', p);
    }
    var a = localStorage.getItem('data-md-color-scheme');
    if (a == null) {
        // alert("未设置主题");
        a = "slate";
        localStorage.setItem("data-md-color-scheme", a);
    }
    document.body.setAttribute('data-md-color-scheme', a);
    // updateScheme();
    updateBoxFontColor();
})()