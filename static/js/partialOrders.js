axios.get('/partial_order/po-groups')
    .then((response) => {
            console.log(response.data)
            let colorMap = new Map(Object.entries(response.data['colorMap']))
            let partialOrderGroups = response.data['groups']

            for (let i = 0; i < partialOrderGroups.length; i++) {
                drawPartialOrder(partialOrderGroups[i], colorMap)
            }
        }
    );

function drawPartialOrder(group, colorMap) {
    let svg = d3.selectAll("#rect1").append("svg").attr("width", 800).attr("height", 200)
    svg.append('polygon')
        .attr('points', "50,50 150,50 175,75 150,100 50,100")
        .attr('fill', colorMap.get(group['cases'][0]['events'][0]['activity']))

    svg.append('text')
        .attr('x', 70)
        .attr('y', 80)
        .attr('stroke', 'black')
        .text(group['cases'][0]['events'][0]['activity'])

    for (let j = 1; j < group['cases'][0]['events'].length; j++) {
        svg.append('polygon')
            .attr('points', `${50 + j * 110},50 ${150 + j * 110},50 ${175 + j * 110},75 ${150 + j * 110},100 ${50 + j * 110},100 ${75 + j * 110},75`)
            .attr('fill', colorMap.get(group['cases'][0]['events'][j]['activity']))

        svg.append('text')
            .attr('x', 80 + j * 110)
            .attr('y', 80)
            .attr('stroke', 'black')
            .text(group['cases'][0]['events'][j]['activity'])
    }
}

function getColors() {
    return [
        '#EE6352',
        '#59CD90',
        '#3FA7D6',
        '#FAC05E',
        '#F79D84',
        '#53A548',
        '#804E49',
        '#A69CAC',
        '#BAF2D8',
        '#9F2042',
        '#788585',
        '#478978',
        '#FA7921',
        '#5BC0EB'
    ]
}

