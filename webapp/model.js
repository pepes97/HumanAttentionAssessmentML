//import * as tf from './tfjs.js';

let attentionModel;
let faceDetectionModel;

async function init(){

    attentionModel = await tf.loadGraphModel('tfjs_vgg16_model/model.json');
    faceDetectionModel = await blazeface.load();


    document.getElementById("loading").hidden = true;
    // JavaScript

    var video = document.getElementById("video");
    try{
        const s = await navigator.mediaDevices.getUserMedia({video: {width:600, height:600}})
        //console.log(s)
        handleVideo(s);
    }
    catch(e){
        //console.log(e.toString())
    }
    function handleVideo(stream){
        //window.URL.createObjectURL()
        window.stream = stream;
        video.srcObject = stream;
    }
    function videoError(e){

    }

    const canvas = document.getElementById("canvas");
    let ctx = canvas.getContext("2d");


    // scale the canvas accordingly
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    // draw the video at that frame
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    // convert it to a usable data URL
    const dataURL = canvas.toDataURL();
}

init()

setInterval(function(){
    var video = document.getElementById("video")
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    // scale the canvas accordingly
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    // draw the video at that frame
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    // convert it to a usable data URL
    const dataURL = canvas.toDataURL();

    
    var img = new Image;
    img.src = dataURL;
    img.onload = async () => {
        const predictionBBox = await faceDetectionModel.estimateFaces(video, false);
        //console.log(predictionBBox);

        ctx.drawImage(img, 0, 0);

        tf.engine().startScope()

        var t = tf.browser.fromPixels(img)
        var t = t.resizeBilinear([128,128])
        t = t.expandDims()
        const b = tf.scalar(255);
        t = t.div(b);
        let pred = attentionModel.predict(t)
        let index = pred.argMax(1)
        const tensorData = index.dataSync();
        //console.log(tensorData[0]);
        let classnames = ['center', 'down', "left", "right", "up"]
        let answer = classnames[tensorData[0]] 
        if(answer ==='center'){
            answer = 'heedful';
        }
        else{
            answer = 'not heedful';
        }

        let div = document.getElementById("answer");
        div.textContent = answer;
        if(answer === 'heedful'){
            div.style.color = "green";
        }
        else{
            div.style.color = "red";
        }

        predictionBBox.forEach(pred => {
            ctx.beginPath();
            ctx.lineWidth = "4";
            if(answer === 'heedful'){
                ctx.strokeStyle = "green";
            }
            else{
                ctx.strokeStyle = "red";
            }
            ctx.rect(
                pred.topLeft[0],
                pred.topLeft[1],
                pred.bottomRight[0] - pred.topLeft[0],
                pred.bottomRight[1] - pred.topLeft[1]
            )
            ctx.stroke();
    
            //ctx.fillStyle = "red";
            //pred.landmarks.forEach((landmark) => {
            //    ctx.fillRect(landmark[0], landmark[1], 5, 5);
            //})
        })

        tf.engine().endScope()
    }

    
}, 200)