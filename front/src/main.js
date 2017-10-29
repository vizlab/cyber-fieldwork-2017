import colormap from 'colormap';

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


Plotly.newPlot('plotlyDiv', [], layout);

fetch('data.json')
    .then(response => response.json())
    .then((json) => {
        console.log('start!');
       let playIndex = 0;
        setInterval(() => {
            if (playIndex === json.length) {
                playIndex = 0;
            }
            draw(json[playIndex]);
            draw3D(json[playIndex]);
            playIndex++;
            console.log(playIndex);
      }, 50);
        console.log('over!');
  });

function draw(vecArray) {
    const colors = colormap({
        colormap: 'jet',
        nshades: 701,
        format: 'hex',
        alpha: 1
    });
    const ctx = document.getElementById('app').getContext('2d');
    for (let i = 0; i < 100; i++) {
        for (let j = 0; j < 100; j++) {
            ctx.fillStyle = colors[parseInt(vecArray[i][j])];
            ctx.fillRect(i*5, j*5, 5, 5);
        }
    }
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
