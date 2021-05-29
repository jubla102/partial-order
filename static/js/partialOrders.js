axios.get('/partial-order/po-groups')
    .then((response) => {
            console.log(response.data)
            let colorMap = new Map(Object.entries(response.data['colorMap']))
            let partialOrderGroups = response.data['groups']

            for (let i = 0; i < partialOrderGroups.length; i++) {
                drawPartialOrder(i, partialOrderGroups[i], colorMap)
            }
        }
    );

function drawPartialOrder(groupNumber, group, colorMap) {
    let svg = d3.selectAll(`#rect${groupNumber}`).append("svg").attr("width", 800).attr("height", 200)
    svg.append('polygon')
        .attr('points', "50,50 150,50 175,75 150,100 50,100")
        .attr('fill', colorMap.get(group['cases'][0]['events'][0]['activity']))

    svg.append('text')
        .attr('x', 70)
        .attr('y', 80)
        .attr('stroke', 'black')
        .text(group['cases'][0]['events'][0]['activity'])

    for (let i = 1; i < group['cases'][0]['events'].length; i++) {
        svg.append('polygon')
            .attr('points', `${50 + i * 110},50 ${150 + i * 110},50 ${175 + i * 110},75 ${150 + i * 110},100 ${50 + i * 110},100 ${75 + i * 110},75`)
            .attr('fill', colorMap.get(group['cases'][0]['events'][i]['activity']))

        svg.append('text')
            .attr('x', 80 + i * 110)
            .attr('y', 80)
            .attr('stroke', 'black')
            .text(group['cases'][0]['events'][i]['activity'])
    }
}
