import colormap from 'colormap';
import $ from 'jquery';
import 'babel-polyfill';

import { getLayout } from './utils';
import { DIFFUSION, LOCK_EXCHANGE } from "./datatype-constants";

Plotly.newPlot('plotlyDiv', [], {});

const renderer = {
    type : "cycle", //0-cycle, 1-slider
    dataType : DIFFUSION, //0-diffusion 1-convaction 2-convection-diffusion 3-lock-exchange
    typeFile : [
        {
            fileNames: ["diffusion.json", "gradient-diffusion.json"],
            canvasWidth: 500,
            canvasHeight: 500
        },
        {
            fileNames: ["convection.json", "gradient-convection.json"],
            canvasWidth: 500,
            canvasHeight: 500
        },
        {
            fileNames: ["convection-diffusion.json", "gradient-convection-diffusion.json"],
            canvasWidth: 500,
            canvasHeight: 500
        },
        {
            fileNames: ["lock-exchange-993-nonB.json", "gradient-lock-exchange-993-nonB.json"],
            canvasWidth: 885,
            canvasHeight: 450
        },
    ],
    cycleId : 0, //the cycle event id
    stepId : 0,
    vData : {},
    setting : {},
    colors : colormap({
        colormap: 'jet',
        nshades: 701,
        format: 'hex',
        alpha: 1
    }),
    canvas : document.getElementById('app'),
    ctx : document.getElementById('app').getContext('2d'),

    init : function() {
        const typeFile = this.typeFile[this.dataType];
        this.canvas.width = typeFile.canvasWidth;
        this.canvas.height = typeFile.canvasHeight;
        const fileNames = typeFile.fileNames;

        const layout = getLayout(this.dataType);
        Plotly.relayout('plotlyDiv', layout)

        fetch(fileNames[0]).then(response => response.json()).then(jsonData => {
            this.vData['scalar'] = jsonData;
        });
        return fetch(fileNames[1]).then(response => response.json()).then(jsonData => {
            this.vData['gradient'] = jsonData['data'];
            this.setting['xGrad'] = jsonData['x_grad_max'];
            this.setting['yGrad'] = jsonData['y_grad_max'];
            this.setting['sampling_interval'] = jsonData['sampling_interval']
        });
    },

    //cycle start
    cycleInit : function() {
        renderer.type = 'cycle';
        this.intervalId = setInterval(() => {
            if (this.stepId === this.vData['scalar'].length) {
                this.stepId = 0;
            }
            this.printGraph(this.stepId);
            $("#slider-icon").val(this.stepId);
            $("#slider-value").text(this.stepId);
            this.stepId++;
        }, 500);
    },

    //stop cycle
    cyclePause : function() {
        clearInterval(this.intervalId);
    },

    //draw all the graph, including vector and 3Dgraph
    printGraph : function(timeStep) {
        this.drawVector(this.vData['scalar'][timeStep], this.vData['gradient'][timeStep], this.setting['xGrad'], this.setting['yGrad'], this.setting['sampling_interval']);
        this.draw3D(this.vData['scalar'][timeStep]);
    },

    //draw vector
    drawVector : function(scalarField, gradientField, xGradMax, yGradMax, samplingInterval) {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.beginPath();

        const SCALE = 5;
        const NX = scalarField.length;      // NX is number of sampling points of x-axis
        const NY = scalarField[0].length;   // NY is number of sampling points of y-axis

        for (let x = 0; x < NX; x++) {
            for (let y = 0; y < NY; y++) {
                this.ctx.fillStyle = this.colors[parseInt(scalarField[x][y])];
                this.ctx.fillRect(x * SCALE, y * SCALE, SCALE, SCALE);
            }
        }

        for (let x = 0; x < NX / samplingInterval; x++) {
            for (let y = 0; y < NY / samplingInterval; y++) {
                const xGrad = gradientField.x[x][y];
                const yGrad = - gradientField.y[x][y];
                const theta = - Math.atan2(yGrad, xGrad);
                const r = 50 * Math.sqrt(Math.pow(xGrad / xGradMax,2) + Math.pow(yGrad / yGradMax,2));
                if (r < 1) {
                    continue;
                }
                const p0 = {x: x * samplingInterval * SCALE, y: y * samplingInterval  * SCALE};
                const p1 = {x: (x * samplingInterval - r * Math.cos(theta)) * SCALE, y: (y * samplingInterval - r * Math.sin(theta)) * SCALE };
                this.drawLineWithArrowhead(p0, p1, 3, this.ctx);
            }
        }
        this.ctx.stroke();
    },

    //draw the arrow in vector
    drawLineWithArrowhead : function(p0, p1, headLength, ctx) {
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

        this.ctx.beginPath();
        // draw the line from p0 to p1
        this.ctx.moveTo(p0.x, p0.y);
        this.ctx.lineTo(p1.x, p1.y);
        // draw partial arrowhead at 225 degrees
        this.ctx.moveTo(p1.x, p1.y);
        this.ctx.lineTo(x225, y225);
        // draw partial arrowhead at 135 degrees
        this.ctx.moveTo(p1.x, p1.y);
        this.ctx.lineTo(x135, y135);
        // stroke the line and arrowhead
        this.ctx.stroke();
    },

    //draw 3D graph
    draw3D : function(vecArray) {
        const data = [{
            z: vecArray,
            type: 'surface',
            autocolorscale: false,
            cauto: false,
            cmax: 700,
            cmin: 0,
        }];
        if (this.dataType === LOCK_EXCHANGE) {
            data[0].cmax = 100;
            data[0].cmin = -50;
        }

        const plotDiv = document.getElementById('plotlyDiv');
        plotDiv.data = data;
        Plotly.redraw('plotlyDiv');
    },
};

(async function() {
    await renderer.init();
    renderer.cycleInit();
})();

$("#slider-icon").on("input", function() {
    const index = $("#slider-icon").val();
    $("#slider-value").text(index);
    renderer.cyclePause();
    renderer.type = 'slider';
    renderer.stepId = index;
    renderer.printGraph(index);
});

$("#auto").on("click", function() {
    if (renderer.type === "cycle") {
        renderer.cyclePause();
    }
    renderer.cycleInit();
});

$("#typeChange input").on("change", async function() {
    const datatype = Number($("input[name='datatype']:checked").val());
    if (datatype !== renderer.datatype) {
        if (renderer.type === "cycle") {
            renderer.cyclePause();
        }
        renderer.dataType = datatype;
        await renderer.init();
        renderer.stepId = 0;
        renderer.cycleInit();
    }
});
