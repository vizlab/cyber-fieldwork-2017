import { LOCK_EXCHANGE } from "./datatype-constants";

export const getLayout = (dataType) => {
    const layout = {
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

    if (dataType === 3) {
        layout.scene.xaxis.range = [0, 100];
        layout.scene.yaxis.range = [0, 200];
        layout.scene.zaxis.range = [-50, 150];
    }

    return layout;
}

