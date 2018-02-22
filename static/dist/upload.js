$('#my-awesome-dropzone').on('sucess', function(){
var arg = Array.prototype.slice.call(arguments);
console.log(arg);
})