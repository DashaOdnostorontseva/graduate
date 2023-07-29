$('#sendPost').on( "click",function (){
    $.ajax({
        url: '/podpis',
        method: 'post',
        dataType: 'html',
        success: function(data){
            if (data=='OK') {
                console.log('SUCCESS')
            }
        }
    })
})