$( '#logout_link').on( 'click',function (){
    loader.showLoader();
    $.ajax( {
        url: 'index.html',
        type: 'post',
         dataType: 'json',
        success: function ( data ){
            if ( 'ok' == data.status ){
                loader.hideLoader();
                window.location.href = "index.html";
            }
        }
    })
});
