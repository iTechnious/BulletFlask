function location_change(location, back=false) {
    let loader = setTimeout(() => {  //delay to prevent loader from flashing
        document.getElementById("page-load").classList.add("active");},
    150);

    //location = location.slice(6)
    console.log(location);
    if(location == null) { location = "/"; }
    if(!back) { window.history.pushState(location, "", location); console.log("added " + location); }

    document.getElementById("create-location").value = location.slice(6);

    fetch("/api/content/get/?html&location=" + location.slice(6))
    .then(
        response => response.text()
            .then((res) => { document.getElementById("forum-contents").innerHTML = res
                let text = "  " + document.getElementById("thread-contents").innerHTML;
                let html = converter.makeHtml(text);
                document.getElementById("thread-contents").innerHTML = html;
                document.querySelectorAll("code").forEach( (ele) => {
                    //add copy button to code blocks
                })
            })
            .then(clearTimeout(loader)) //prevents animation to play if this is done too early
            .then(document.getElementById("page-load").classList.remove("active"))
    );

    path = location.slice(6).split("/").filter((ele) => {return ele != ""})

    console.log(path);

    let location_data;
    fetch("/api/content/get_data/?breadcrumb&location=" + location.slice(6))
        .then( response => response.json().then(res => location_data = res).then( document.querySelectorAll('.auto-breadcrumb').forEach(e => e.remove()) ))
        .then(() => {
            for (let i = 0; i < path.length; i++) {
                console.log(i);
                link = document.getElementById("start-link").cloneNode();
                href = "/" + path.slice(0, path.length - i).join("/") + "/";
                console.log(href);
                link.setAttribute('onclick', 'location_change("/forum'+href+'")');
                link.innerHTML = location_data[i]["name"];
                link.classList.add("auto-breadcrumb");
                document.getElementById("start-link").after(link);
            }
        });
}

window.onpopstate = () => {
    location_change(window.history.state, back=true);
}

location_change(window.location.pathname, back=true);

var converter = new showdown.Converter({});