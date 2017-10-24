fetch('u0.json')
    .then(response => response.json())
    .then((json) => {
        draw(json);
  });

function draw(vecArray) {
    var ctx = document.getElementById('app').getContext('2d');
    for (var i = 0; i < 300; i++) {
        for (var j = 0; j < 300; j++) {
            console.log(vecArray[i][j]);
            var color = getColor(vecArray[i][j]);
        }
    }
}

function getColor(num) {
    var low = 300;
    var range = 400;
    console.log(num);
}
