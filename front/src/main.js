import colormap from 'colormap';
import $ from 'jquery';
import slider from 'bootstrap-slider';

const layout = {
    title: 'Diffusion Equation Simulation',
    autosize: false,
    width: 500,
    height: 500,
    scene: {
        aspectratio: {
            x: 1,
            y: 1,
            z: 1,
        },
        xaxis: {
            range: [0, 100],
        },
        yaxis: {
            range: [0, 100],
        },
        zaxis: {
            range: [0, 700],
        },
        camera: {
            up: {
                x: 0,
                y: 0,
                z: 0
            },
            center: {
                x: 0,
                y: 0,
                z: 0
            },
            eye: {
                x: -1.8,
                y: -1.8,
                z: 1.5
            }
        }
    },
    margin: {
        l: 35,
        r: 20,
        b: 35,
        t: 60,
    }
};

$('#ex6').slider({
    formatter: function(value) {
        return 'Current value: ' + value;
    }
});

Plotly.newPlot('plotlyDiv', [], layout);

const scalarFetch = fetch('data.json').then(response => response.json());
const gradientFetch = fetch('gradient-fields.json').then(response => response.json());

Promise.all([scalarFetch, gradientFetch]).then((jsonList) => {
    const scalarFields = jsonList[0];
    const gradientFields = jsonList[1].data;
    const xGradMax = jsonList[1].x_grad_max;
    const yGradMax = jsonList[1].y_grad_max;

    let playIndex = 0;
    setInterval(() => {
        if (playIndex === scalarFields.length) {
            playIndex = 0;
        }
        drawVector(scalarFields[playIndex], gradientFields[playIndex], xGradMax, yGradMax);
        draw3D(scalarFields[playIndex]);
        playIndex++;
    }, 500);
});

function drawVector(scalarField, gradientField, xGradMax, yGradMax) {
    const colors = colormap({
        colormap: 'jet',
        nshades: 701,
        format: 'hex',
        alpha: 1
    });
    const canvas = document.getElementById('app');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();

    const SCALE = 5;
    for (let x = 0; x < 100; x++) {
        for (let y = 0; y < 100; y++) {;
            ctx.fillStyle = colors[parseInt(scalarField[x][y])];
            ctx.fillRect(x * SCALE, y * SCALE, SCALE, SCALE);
        }
    }

    const arrowInterval = 5;
    for (let x = 0; x < 100; x += arrowInterval) {
        for (let y = 0; y < 100; y += arrowInterval) {
            const xGrad = gradientField.x[x][y];
            const yGrad = - gradientField.y[x][y];
            const theta = - Math.atan2(yGrad, xGrad);
            const r = 50 * Math.sqrt(Math.pow(xGrad / xGradMax,2) + Math.pow(yGrad / yGradMax,2));
            if (r < 1) {
                continue;
            }
            const p0 = {x: x * SCALE, y: y * SCALE};
            const p1 = {x: (x - r * Math.cos(theta)) * SCALE, y: (y - r * Math.sin(theta)) * SCALE };
            drawLineWithArrowhead(p0, p1, 3, ctx);
        }
    }
    ctx.stroke();
}

// ref: https://stackoverflow.com/questions/26804679/how-can-i-draw-arrows-on-a-canvas-with-mouse
function drawLineWithArrowhead(p0, p1, headLength, ctx){
    const degreesInRadians225 = 225 * Math.PI / 180;
    const degreesInRadians135 = 135 * Math.PI / 180;

    // calc the angle of the line
    const dx = p1.x - p0.x;
    const dy = p1.y - p0.y;
    const angle = Math.atan2(dy, dx);

    // calc arrowhead points
    const x225 = p1.x + headLength * Math.cos(angle + degreesInRadians225);
    const y225 = p1.y + headLength * Math.sin(angle + degreesInRadians225);
    const x135 = p1.x + headLength * Math.cos(angle + degreesInRadians135);
    const y135 = p1.y + headLength * Math.sin(angle + degreesInRadians135);

    ctx.beginPath();
    // draw the line from p0 to p1
    ctx.moveTo(p0.x, p0.y);
    ctx.lineTo(p1.x, p1.y);
    // draw partial arrowhead at 225 degrees
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(x225, y225);
    // draw partial arrowhead at 135 degrees
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(x135, y135);
    // stroke the line and arrowhead
    ctx.stroke();
}

function draw3D(vecArray) {
    const data = [{
        z: vecArray,
        type: 'surface',
        autocolorscale: false,
        cauto: false,
        cmax: 700,
        cmin: 0,
    }];

    const plotDiv = document.getElementById('plotlyDiv');
    plotDiv.data = data;
    Plotly.redraw('plotlyDiv');
}
