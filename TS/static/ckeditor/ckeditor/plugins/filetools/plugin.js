<<<<<<< HEAD
﻿/*
 Copyright (c) 2003-2015, CKSource - Frederico Knabben. All rights reserved.
 For licensing, see LICENSE.md or http://ckeditor.com/license
*/
(function(){function h(a){this.editor=a;this.loaders=[]}function i(a,b,c){var d=a.config.fileTools_defaultFileName;this.editor=a;this.lang=a.lang;"string"===typeof b?(this.data=b,this.file=k(this.data),this.loaded=this.total=this.file.size):(this.data=null,this.file=b,this.total=this.file.size,this.loaded=0);c?this.fileName=c:this.file.name?this.fileName=this.file.name:(a=this.file.type.split("/"),d&&(a[0]=d),this.fileName=a.join("."));this.uploaded=0;this.status="created";this.abort=function(){this.changeStatus("abort")}}
function k(a){var b=a.match(j)[1],a=a.replace(j,""),a=atob(a),c=[],d,f,e,g;for(d=0;d<a.length;d+=512){f=a.slice(d,d+512);e=Array(f.length);for(g=0;g<f.length;g++)e[g]=f.charCodeAt(g);f=new Uint8Array(e);c.push(f)}return new Blob(c,{type:b})}CKEDITOR.plugins.add("filetools",{lang:"cs,da,de,en,eo,fr,gl,it,ko,ku,nb,nl,pl,pt-br,ru,sv,tr,zh,zh-cn",beforeInit:function(a){a.uploadRepository=new h(a);a.on("fileUploadRequest",function(a){a=a.data.fileLoader;a.xhr.open("POST",a.uploadUrl,!0)},null,null,5);
a.on("fileUploadRequest",function(a){var a=a.data.fileLoader,c=new FormData;c.append("upload",a.file,a.fileName);a.xhr.send(c)},null,null,999);a.on("fileUploadResponse",function(a){var c=a.data.fileLoader,d=c.xhr,f=a.data;try{var e=JSON.parse(d.responseText);e.error&&e.error.message&&(f.message=e.error.message);e.uploaded?(f.fileName=e.fileName,f.url=e.url):a.cancel()}catch(g){f.message=c.lang.filetools.responseError,window.console&&window.console.log(d.responseText),a.cancel()}},null,null,999)}});
h.prototype={create:function(a,b){var c=this.loaders.length,d=new i(this.editor,a,b);d.id=c;this.loaders[c]=d;this.fire("instanceCreated",d);return d},isFinished:function(){for(var a=0;a<this.loaders.length;++a)if(!this.loaders[a].isFinished())return!1;return!0}};i.prototype={loadAndUpload:function(a){var b=this;this.once("loaded",function(c){c.cancel();b.once("update",function(a){a.cancel()},null,null,0);b.upload(a)},null,null,0);this.load()},load:function(){var a=this,b=this.reader=new FileReader;
a.changeStatus("loading");this.abort=function(){a.reader.abort()};b.onabort=function(){a.changeStatus("abort")};b.onerror=function(){a.message=a.lang.filetools.loadError;a.changeStatus("error")};b.onprogress=function(b){a.loaded=b.loaded;a.update()};b.onload=function(){a.loaded=a.total;a.data=b.result;a.changeStatus("loaded")};b.readAsDataURL(this.file)},upload:function(a){a?(this.uploadUrl=a,this.xhr=new XMLHttpRequest,this.attachRequestListeners(),this.editor.fire("fileUploadRequest",{fileLoader:this})&&
this.changeStatus("uploading")):(this.message=this.lang.filetools.noUrlError,this.changeStatus("error"))},attachRequestListeners:function(){var a=this,b=this.xhr;a.abort=function(){b.abort()};b.onabort=function(){a.changeStatus("abort")};b.onerror=function(){a.message=a.lang.filetools.networkError;a.changeStatus("error")};b.onprogress=function(b){a.uploaded=b.loaded;a.update()};b.onload=function(){a.uploaded=a.total;if(200>b.status||299<b.status)a.message=a.lang.filetools["httpError"+b.status],a.message||
(a.message=a.lang.filetools.httpError.replace("%1",b.status)),a.changeStatus("error");else{for(var c={fileLoader:a},d=["message","fileName","url"],f=a.editor.fire("fileUploadResponse",c),e=0;e<d.length;e++){var g=d[e];"string"===typeof c[g]&&(a[g]=c[g])}!1===f?a.changeStatus("error"):a.changeStatus("uploaded")}}},changeStatus:function(a){this.status=a;if("error"==a||"abort"==a||"loaded"==a||"uploaded"==a)this.abort=function(){};this.fire(a);this.update()},update:function(){this.fire("update")},isFinished:function(){return!!this.status.match(/^(?:loaded|uploaded|error|abort)$/)}};
CKEDITOR.event.implementOn(h.prototype);CKEDITOR.event.implementOn(i.prototype);var j=/^data:(\S*?);base64,/;CKEDITOR.fileTools||(CKEDITOR.fileTools={});CKEDITOR.tools.extend(CKEDITOR.fileTools,{uploadRepository:h,fileLoader:i,getUploadUrl:function(a,b){var c=CKEDITOR.tools.capitalize;return b&&a[b+"UploadUrl"]?a[b+"UploadUrl"]:a.uploadUrl?a.uploadUrl:b&&a["filebrowser"+c(b,1)+"UploadUrl"]?a["filebrowser"+c(b,1)+"UploadUrl"]+"&responseType=chioma":a.filebrowserUploadUrl?a.filebrowserUploadUrl+"&responseType=chioma":
=======
﻿/*
 Copyright (c) 2003-2015, CKSource - Frederico Knabben. All rights reserved.
 For licensing, see LICENSE.md or http://ckeditor.com/license
*/
(function(){function h(a){this.editor=a;this.loaders=[]}function i(a,b,c){var d=a.config.fileTools_defaultFileName;this.editor=a;this.lang=a.lang;"string"===typeof b?(this.data=b,this.file=k(this.data),this.loaded=this.total=this.file.size):(this.data=null,this.file=b,this.total=this.file.size,this.loaded=0);c?this.fileName=c:this.file.name?this.fileName=this.file.name:(a=this.file.type.split("/"),d&&(a[0]=d),this.fileName=a.join("."));this.uploaded=0;this.status="created";this.abort=function(){this.changeStatus("abort")}}
function k(a){var b=a.match(j)[1],a=a.replace(j,""),a=atob(a),c=[],d,f,e,g;for(d=0;d<a.length;d+=512){f=a.slice(d,d+512);e=Array(f.length);for(g=0;g<f.length;g++)e[g]=f.charCodeAt(g);f=new Uint8Array(e);c.push(f)}return new Blob(c,{type:b})}CKEDITOR.plugins.add("filetools",{lang:"cs,da,de,en,eo,fr,gl,it,ko,ku,nb,nl,pl,pt-br,ru,sv,tr,zh,zh-cn",beforeInit:function(a){a.uploadRepository=new h(a);a.on("fileUploadRequest",function(a){a=a.data.fileLoader;a.xhr.open("POST",a.uploadUrl,!0)},null,null,5);
a.on("fileUploadRequest",function(a){var a=a.data.fileLoader,c=new FormData;c.append("upload",a.file,a.fileName);a.xhr.send(c)},null,null,999);a.on("fileUploadResponse",function(a){var c=a.data.fileLoader,d=c.xhr,f=a.data;try{var e=JSON.parse(d.responseText);e.error&&e.error.message&&(f.message=e.error.message);e.uploaded?(f.fileName=e.fileName,f.url=e.url):a.cancel()}catch(g){f.message=c.lang.filetools.responseError,window.console&&window.console.log(d.responseText),a.cancel()}},null,null,999)}});
h.prototype={create:function(a,b){var c=this.loaders.length,d=new i(this.editor,a,b);d.id=c;this.loaders[c]=d;this.fire("instanceCreated",d);return d},isFinished:function(){for(var a=0;a<this.loaders.length;++a)if(!this.loaders[a].isFinished())return!1;return!0}};i.prototype={loadAndUpload:function(a){var b=this;this.once("loaded",function(c){c.cancel();b.once("update",function(a){a.cancel()},null,null,0);b.upload(a)},null,null,0);this.load()},load:function(){var a=this,b=this.reader=new FileReader;
a.changeStatus("loading");this.abort=function(){a.reader.abort()};b.onabort=function(){a.changeStatus("abort")};b.onerror=function(){a.message=a.lang.filetools.loadError;a.changeStatus("error")};b.onprogress=function(b){a.loaded=b.loaded;a.update()};b.onload=function(){a.loaded=a.total;a.data=b.result;a.changeStatus("loaded")};b.readAsDataURL(this.file)},upload:function(a){a?(this.uploadUrl=a,this.xhr=new XMLHttpRequest,this.attachRequestListeners(),this.editor.fire("fileUploadRequest",{fileLoader:this})&&
this.changeStatus("uploading")):(this.message=this.lang.filetools.noUrlError,this.changeStatus("error"))},attachRequestListeners:function(){var a=this,b=this.xhr;a.abort=function(){b.abort()};b.onabort=function(){a.changeStatus("abort")};b.onerror=function(){a.message=a.lang.filetools.networkError;a.changeStatus("error")};b.onprogress=function(b){a.uploaded=b.loaded;a.update()};b.onload=function(){a.uploaded=a.total;if(200>b.status||299<b.status)a.message=a.lang.filetools["httpError"+b.status],a.message||
(a.message=a.lang.filetools.httpError.replace("%1",b.status)),a.changeStatus("error");else{for(var c={fileLoader:a},d=["message","fileName","url"],f=a.editor.fire("fileUploadResponse",c),e=0;e<d.length;e++){var g=d[e];"string"===typeof c[g]&&(a[g]=c[g])}!1===f?a.changeStatus("error"):a.changeStatus("uploaded")}}},changeStatus:function(a){this.status=a;if("error"==a||"abort"==a||"loaded"==a||"uploaded"==a)this.abort=function(){};this.fire(a);this.update()},update:function(){this.fire("update")},isFinished:function(){return!!this.status.match(/^(?:loaded|uploaded|error|abort)$/)}};
CKEDITOR.event.implementOn(h.prototype);CKEDITOR.event.implementOn(i.prototype);var j=/^data:(\S*?);base64,/;CKEDITOR.fileTools||(CKEDITOR.fileTools={});CKEDITOR.tools.extend(CKEDITOR.fileTools,{uploadRepository:h,fileLoader:i,getUploadUrl:function(a,b){var c=CKEDITOR.tools.capitalize;return b&&a[b+"UploadUrl"]?a[b+"UploadUrl"]:a.uploadUrl?a.uploadUrl:b&&a["filebrowser"+c(b,1)+"UploadUrl"]?a["filebrowser"+c(b,1)+"UploadUrl"]+"&responseType=json_file":a.filebrowserUploadUrl?a.filebrowserUploadUrl+"&responseType=json_file":
>>>>>>> 01ab2abe6fcb2d52e11f33de361fc614a5915e57
null},isTypeSupported:function(a,b){return!!a.type.match(b)}})})();