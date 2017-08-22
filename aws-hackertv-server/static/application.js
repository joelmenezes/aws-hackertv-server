
App.onLaunch = function(options) {
    
    var url = "http://www.hackertv.io/jsonTVML";
    get(url).then(JSON.parse).then(function(response) {
        console.log(response);
        showAPIResponse(response);
    })
    
}


App.onWillResignActive = function() {

}

App.onDidEnterBackground = function() {

}

App.onWillEnterForeground = function() {
    
}

App.onDidBecomeActive = function() {
    
}

App.onWillTerminate = function() {
    
}


/**
 * This convenience funnction returns an alert template, which can be used to present errors to the user.
 
var createAlert = function(title, description) {

    var alertString = `<?xml version="1.0" encoding="UTF-8" ?>
        <document>
          <alertTemplate>
            <title>${title}</title>
            <description>${description}</description>
          </alertTemplate>
        </document>`

    var parser = new DOMParser();

    var alertDoc = parser.parseFromString(alertString, "application/xml");

    return alertDoc
}
*/


function get(url) {
    
    return new Promise(function(resolve, reject) {
    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
        resolve(this.responseText);
    };
    xhr.onerror = reject;
    xhr.open('GET', url);
    xhr.send();
    });
    
}
/*
function reqListener() {
    console.log(this.responseText);
    var response = JSON.parse(this.responseText);
    showAPIResponse(response);
}

function callServerForURL(url) {
    var xhr = new XMLHttpRequest();
    xhr.addEventListener("load", reqListener);
    xhr.open("GET", url);
    xhr.send();
}
*/
function playMedia(url, mediaType) {
    var singleVideo = new MediaItem(mediaType, url);
    var videoList = new Playlist();
    videoList.push(singleVideo);
    var myPlayer = new Player();
    myPlayer.playlist = videoList;
    myPlayer.present();
    console.log('PLaying');
}

function playVideo(url) {
    console.log(url);
    openURL(url);
    var okay = canOpenURL(url);
    console.log(okay);
}

function showAPIResponse(response){
    var results = response;
    var alertString = `

    <document>
    <searchTemplate>
    <collectionList>
    <grid>
    <header>
    <description>Popular</description>
    </header>
    <section>
    `
    for (i in results){
        alertString += `<lockup onselect = "playVideo('${results[i].url}')"><img src= "${results[i].image}" width = "274" height = "182" /><title> ${results[i].title}</title><subtitle>Points: ${results[i].points} | Posted: ${results[i].created_at}</subtitle></lockup>`
    }
    alertString += `
    </section>
    </grid>
    </collectionList>
    </searchTemplate>
    </document>
`
    console.log(alertString);
    var parser = new DOMParser();
    var alertDoc = parser.parseFromString(alertString, "application/xml");
    navigationDocument.pushDocument(alertDoc);
}
/*
 for (i in results){
 templateXML += ‘<lockup id=”‘ + results[i].created_at_i+ ‘”><title style=”color:rgba(255, 255, 255, 0.5);”>’ + htmlSpecialChars(results[i].title) + ‘</title><subtitle style=”color:rgba(255, 255, 255, 0.5);”> Votes ‘ + results[i].hits + ‘</subtitle></lockup>';
 
 }
 */
