/* 
Fonction permettant d'afficher les fichiers
renseignéspar l'utilisateur
*/
function FileSelected(file)
{
    document.getElementById('file_list').innerHTML = ""
    if (file != undefined) {
        for (i=0;i<file.length;i++) {
            document.getElementById('file_list').innerHTML += "<li>"+file[i]["name"]+"</li>"
        }
    }
}

/*
Fonction permettant d'afficher ou de cacher
une div en fonction de son id.
*/
function show_rename(id_div) {
    elt = document.getElementById(id_div);
    if (elt.style.display == "block") {
        elt.style.display = "none";
    } else {
        elt.style.display = "block";
    }
}
