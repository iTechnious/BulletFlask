function location_change(location, back=false) {
    let loader = setTimeout(() => {  //delay to prevent loader from flashing
        document.getElementById("page-load").classList.add("active");},
    150);

    if(location == null) { location = "/"; }
    if(!back) { window.history.pushState(location, "", "/forum/"+ location); }

    document.getElementById("create-location").value = location;

    fetch("/api/content/get/?html&location=" + location)
    .then(
        response => response.text()
        .then((res) => { document.getElementById("forum-contents").innerHTML = res
            try {let text = "  " + document.getElementById("thread-contents").innerHTML;
                let html = converter.makeHtml(text);

                console.log(html);
                document.getElementById("thread-contents").innerHTML = html;
                document.querySelectorAll("code").forEach( (ele) => {
                    //add copy button to code blocks
                })
                document.querySelectorAll('pre code').forEach((el) => {
                    hljs.highlightElement(el);
                });
                
            } catch {}
        })
        .then(clearTimeout(loader)) //prevents animation to play if this is done early
        .then(document.getElementById("page-load").classList.remove("active"))
        .then(document.getElementById("page-warn").classList.add("hide"))
    ).catch((reason) => {
        console.log(reason);
        document.getElementById("page-warn").classList.remove("hide");
        setTimeout(() => {
            location_change(location, back=back);
        }, 5000)
    });

    let location_data;
    fetch("/api/content/get_data/?breadcrumb&location=" + location)
    .then(response => response.json().then(res => location_data = res)
    .then( document.querySelectorAll('.auto-breadcrumb').forEach(e => e.remove()) ))
    .then(() => {
        location_data.forEach(element => {
            link = document.getElementById("start-link").cloneNode();
            link.setAttribute('onclick', 'location_change("'+element['id']+'")');
            link.innerHTML = element["name"];
            link.classList.add("auto-breadcrumb");
            document.getElementById("start-link").after(link);
        });
    })
    .catch((reason) => {});

    Array.prototype.forEach.call(document.getElementsByClassName("location-autoupdate"), (element) => {
        element.value = location;
    });
}

window.onpopstate = () => {
    let l = window.history.state;
    location_change(l, back=true)
}

let l = window.location.pathname;
if(l.slice(6) == "/") {
    location_change("0");
} else {
    let location = l.slice(6).split("/").filter(n => n);
    location = location.at(-1);
    location_change(location, back=true);
}

var converter = new showdown.Converter({"simplifiedAutoLink": true,
                                        "strikethrough": true, 
                                        "tasklists": true, 
                                        "smoothLivePreview": true, 
                                        "emoji": true});

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.fixed-action-btn');
    M.FloatingActionButton.init(elems, {
        direction: 'top',
        hoverEnabled: false
    });
});
