function FileSelected(file)
{
    document.getElementById('file_list').innerHTML = ""
    if (file != undefined) {
        for (i=0;i<file.length;i++) {
            document.getElementById('file_list').innerHTML += "<li>"+file[i]["name"]+"</li>"
        }
    }
}

function show_rename(id_div) {
    elt = document.getElementById(id_div);
    if (elt.style.display == "none") {
        elt.style.display = "block";
    } else {
        elt.style.display = "none";
    }
}
