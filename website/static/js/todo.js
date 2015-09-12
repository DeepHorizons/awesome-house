xmlhttp=new XMLHttpRequest();
xmlhttp.onreadystatechange=function()
  {
  if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
        var resp = JSON.parse(xmlhttp.responseText);
        var task_date = document.getElementById('date_' + resp['task_id']);
        task_date.innerHTML = resp['date_done'];

        var row = document.getElementById('row_' + resp['task_id']);
        if( row != null){
            if(resp['date_done'] != null){
                row.className = "strikeout";
            } else {
                row.className = "";
            }
        }
    }
  }
function sendCheckBox(cb) {
    xmlhttp.open("POST", "/todos/status", true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send("id=" + cb.getAttribute('data-id') + "&status=" + cb.checked);
}