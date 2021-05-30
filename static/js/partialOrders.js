const START_X = 50
const START_Y = 50
const ACTIVITY_WIDTH = 100
const ACTIVITY_HEIGHT = 50
const GAP = 10
const CORNER_DIAMETER = 25

axios.get('/partial-order/po-groups')
    .then((response) => {
            console.log(response.data)
            let colorMap = new Map(Object.entries(response.data['colorMap']))
            let partialOrderGroups = response.data['groups']

            for (let i = 0; i < partialOrderGroups.length; i++) {
                drawPartialOrder(i, partialOrderGroups[i]['cases'][0]['events'], colorMap)
            }
        }
    );

function drawPartialOrder(groupNumber, events, colorMap) {
    //todo: get the length of the longest trace for width

    let svg = d3.selectAll(`#rect${groupNumber}`).append("svg").attr("width", 8000).attr("height", 200)

    for (let i = 0; i < events.length; i++) {
        if (i === 0) {
            drawStartingEvent(svg, events[i]['activity'], colorMap)
        } else {
            drawEvent(svg, events[i]['activity'], colorMap, i)
        }
    }
}

function drawStartingEvent(svg, activityName, colorMap) {

    svg.append('polygon')
        .attr('points', `${START_X},${START_Y} ${START_X + ACTIVITY_WIDTH},${START_Y} ${START_X + ACTIVITY_WIDTH + CORNER_DIAMETER},${START_Y + CORNER_DIAMETER} ${START_X + ACTIVITY_WIDTH},${START_Y + ACTIVITY_HEIGHT} ${START_X},${START_Y + ACTIVITY_HEIGHT}`)
        .attr('fill', colorMap.get(activityName))

    svg.append('text')
        .attr('x', 70)
        .attr('y', 80)
        .attr('stroke', 'black')
        .text(activityName)
}

function drawEvent(svg, activityName, colorMap, offset) {
    svg.append('polygon')
        .attr('points', `${START_X + offset * (ACTIVITY_WIDTH + GAP)},${START_Y} ${(START_X + ACTIVITY_WIDTH) + offset * (ACTIVITY_WIDTH + GAP)},${START_Y} ${START_X + ACTIVITY_WIDTH + CORNER_DIAMETER + offset * (ACTIVITY_WIDTH + GAP)},${START_Y + CORNER_DIAMETER} ${START_X + ACTIVITY_WIDTH + offset * (ACTIVITY_WIDTH + GAP)},${START_Y + ACTIVITY_HEIGHT} ${START_X + offset * (ACTIVITY_WIDTH + GAP)},${START_Y + ACTIVITY_HEIGHT} ${START_X + CORNER_DIAMETER + offset * (ACTIVITY_WIDTH + GAP)},${START_Y + CORNER_DIAMETER}`)
        .attr('fill', colorMap.get(activityName))

    svg.append('text')
        .attr('x', 80 + offset * 110)
        .attr('y', 80)
        .attr('stroke', 'black')
        .text(activityName)
}
