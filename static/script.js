function FileSelected(e)
{
    file = document.getElementById('fu').files[document.getElementById('fu').files.length - 1];
    document.getElementById('fileName').innerHtml= file.name;
}
