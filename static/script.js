function FileSelected()
{

    document.getElementById('file_list').innerHTML = ""
    file = document.getElementById('getFile').files;
    if (file != undefined) {
        for (i=0;i<file.length;i++) {
            document.getElementById('file_list').innerHTML += "<p>"+file[i]["name"]+"</p>"
        }
    }
}
