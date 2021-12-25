function location_change(location, back=false, version=null) {
    console.log(`Changing location to\nLocation: ${location}\nBack?: ${back}\nversion: ${version}`)
    let loader = setTimeout(() => {  //delay to prevent loader from flashing
        document.getElementById("page-load").classList.add("active");},
    150);
    
    let query;
    let state;
    let state_url;
    if(version != null) {
        query = `/api/content/get/?html&location=${location}&version=${version}`
        state = {"location": location, "version": version};
        state_url = "/forum/"+ location + `?version=${version}`;
    } else {
        query = `/api/content/get/?html&location=${location}`;
        state = {"location": location, "version": version};
        state_url = "/forum/"+ location + "/";
    }
    if(!back) { window.history.pushState(state, "", state_url); }
    
    document.getElementById("create-location").value = location;

    fetch(query)
    .then(
        response => response.text()
        .then((res) => { document.getElementById("forum-contents").innerHTML = res
            try {let text = "  " + document.getElementById("thread-contents").innerHTML;
                let html = converter.makeHtml(text);
                document.getElementById("thread-contents").innerHTML = html;

                document.querySelectorAll("code").forEach( (ele) => {
                    //add copy button to code blocks
                })
                document.querySelectorAll('pre code').forEach((el) => {
                    hljs.highlightElement(el);
                });
                
            } catch {}
        })
        .then(clearTimeout(loader)) //prevents animation from playing if this is done early
        .then(document.getElementById("page-load").classList.remove("active"))
        .then(document.getElementById("page-warn").classList.add("hide"))
    ).catch((reason) => {
        console.log(reason);
        document.getElementById("page-warn").classList.remove("hide");
        setTimeout(() => {
            location_change(location, back=back, version);
        }, 5000)
    });

    let location_data;
    fetch("/api/content/get_data/?breadcrumb&location=" + location)
    .then(response => response.json().then(res => location_data = res)
    .then( document.querySelectorAll('.auto-breadcrumb').forEach(e => e.remove()) ))
    .then(() => {
        var i = 0;
        location_data.forEach(element => {
            link = document.getElementById("start-link").cloneNode();
            link.setAttribute('onclick', 'location_change("'+element['id']+'")');
            if (element["name"].length > 15 && i != 0) {
                link.innerHTML = element["name"].slice(0,15) + "...";
            } else {
                link.innerHTML = element["name"];
            }
            link.classList.add("auto-breadcrumb");
            document.getElementById("start-link").after(link);
            i++;
        });
    })
    .catch((reason) => {});

    Array.prototype.forEach.call(document.getElementsByClassName("location-autoupdate"), (element) => {
        element.value = location;
    });
}

function findGetParameter(parameterName) {  // credit: https://stackoverflow.com/a/5448595
    var result = null,
        tmp = [];
    var items = location.search.substr(1).split("&");
    for (var index = 0; index < items.length; index++) {
        tmp = items[index].split("=");
        if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
    }
    return result;
}

window.onpopstate = () => {
    let l = window.history.state;
    if (l == null) {
        console.log(window.history.url)
        location_change(0, back=true, version=null);
    } else {
        location_change(l.location, back=true, l.version)
    }
}

let l = window.location.pathname;
if(l.slice(6) == "/") {
    location_change("0", back=true, version=null);
} else {
    let location = l.slice(6).split("/").filter(n => n);
    location = location.at(-1);
    location_change(location, back=true, version=findGetParameter("version"));
}

var converter = new showdown.Converter({"simplifiedAutoLink": true,
                                        "strikethrough": true, 
                                        "tasklists": true, 
                                        "smoothLivePreview": true, 
                                        "emoji": true,
                                        "simpleLineBreaks": true});

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.fixed-action-btn');
    M.FloatingActionButton.init(elems, {
        direction: 'top',
        hoverEnabled: false
    });
});
