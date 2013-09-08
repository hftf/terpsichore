postArray = function(array) {
    // path = '/record';
    // var xhr = new XMLHttpRequest();
    // xhr.open('POST', path, true);
    // xhr.send(array);
    string = ""
    for(var  i = 0; i < array.length; i++) {
        array[i] *= 32768
        string += Math.round(array[i]) + ";";
    }
    $.ajax({
        'type' : 'POST',
        'url' : '/record',
        'data' : {'data': string, 'token' : myToken, 'flag' : 'ok'},
        success : function(data){
            console.log(data)
        }
    });
};

onOpened = function() {
    connected = true;
};

onMessage = function(){

}

onError = function(){

}

onClose = function(){

}
