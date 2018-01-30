    // 生成决策树
function createTree() {
    $('#picture').html('');
    $.ajax({
        url:'/action/create',
        type:'GET',
        async:false,
        data:{},
        success:function (data) {
            // console.log(data);
            deal(data)
        },
        error:function (xhr,testStatus) {
            console.log('error')
        }
    })
}

function deal(data) {
    var imgNode = document.createElement('img');
    imgNode.setAttribute('src','data:image/png;base64,'+ data);
    document.getElementById('picture').appendChild(imgNode);
}


// 文件上传
function uploads() {
    $("#uploadfileresult").html('');
    $.ajax({
        url:'/fileup/fileuploaded',
        type:'post',
        async:false,
        data:{},
        success:function (results) {
            addFileResult(results)
        },
        error:function (xhr,testState) {
            console.log('error')
        }
        })

    $("#form1").bind("submit", function(){
    var file=$("#file_sc").val();
    if( file == " " ){
        alert("请选择文件！！！");
        return false;
    }
});
    }


function addFileResult(results) {
// {#    var fileRes = document.createElement('p');#}
// {#    fileRes.innerHTML = results;#}
// {#    document.getElementById('uploadfileresult').appendChild(fileRes);#}
    console.log(results);
    var uploadFileResult = document.getElementById('uploadfileresult');
    var fileRes = document.createElement('p');
    fileRes.innerHTML = 'lican';
    uploadFileResult.appendChild(fileRes)
}

function transdata() {
    $.ajax({
        url:'/action/dealdata',
        type:'POST',
        async:false,
        data:{},
        success:function (results) {
// {#            show(results)#}
            alert(results)
        },
        error:function (xhr,testState) {
            console.log('error')
        }

    })
}

// function show() {
// {#    var imgNode = document.createElement('input');#}
// {#    imgNode.setAttribute('src','data:image/png;base64,'+ data);#}
// {#    document.getElementById('labels').appendChild(imgNode);#}
// }

