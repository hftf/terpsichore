var postArray = function(array) {
    string = "";
    for (var i = 0; i < array.length; i ++) {
        array[i] *= 32768
        string += Math.round(array[i]) + ";";
    }
    
    $.ajax({
        'type': 'POST',
        'url': '/record',
        'data': { 'data': string, 'token': myToken, 'flag': 'ok' },
        success: function(data) {
            console.log(data);
        }
    });
};
