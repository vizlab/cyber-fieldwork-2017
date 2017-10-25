fetch('u0.json')
    .then(response => response.json())
    .then((json) => {
        console.log('start!');
        draw(json);
        console.log('over!');
  });

function draw(vecArray) {
    const ctx = document.getElementById('app').getContext('2d');
    for (let i = 0; i < 100; i++) {
        for (let j = 0; j < 100; j++) {
            ctx.fillStyle = getColor(vecArray[i][j]);
            ctx.fillRect(i*5, j*5, 5, 5);
        }
    }
}

//TODO: think a better color distribution
function getColor(num) {
    let all = parseInt((num-300) / 3);
    let remain = num % 3;

    let colorStr = 'rgb(' + all + ',';
    if (num == 2) {
        colorStr += (all+1) + ',' + (all+1) + ')';
    } else if (num == 1) {
        colorStr += all + ',' + (all+1) + ')';
    } else {
        colorStr += all + ',' + all + ')';
    }
    return colorStr;
}
