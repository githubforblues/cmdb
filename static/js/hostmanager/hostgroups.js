var aHostGroupDelete = document.getElementsByName('hostgroupdelete');

window.onload=function() {

    function hostgroupdelete(obj, hostname, hostgroup) {
        $.ajax({
            url:"/hostgroupdelete/",
            data:{'hostname':hostname, 'hostgroup': hostgroup},
            type:"POST",
            success:function(){
                alert('删除成功');
                // obj.parentNode.parentNode.style.display = "none";
                otr = obj.parentNode.parentNode;
                otr.parentNode.removeChild(otr);
            }
        })
    }

    for (var i = 0; i <= aHostGroupDelete.length; i++) {
        aHostGroupDelete[i].onclick = function () {
            hostgroupdelete(this, this.getAttribute("hostname"), this.getAttribute("hostgroup"));
        }
    }
};
















