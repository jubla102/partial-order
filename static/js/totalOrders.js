const EVENT_WIDTH = 125
const EVENT_HEIGHT = 50
const GAP = 10
const EVENT_DIAMETER = 25
const EVENTS_KEY = 'events'
const ACTIVITY_KEY = 'concept:name'

axios.get('/partial-order/test')
    .then((response) => {
            let colorMap = new Map(Object.entries(response.data['colors']))
            let combinations = response.data['combinations']

            for (let i = 0; i < combinations.length; i++) {
                drawTotalOrders(i, combinations[i], colorMap)
            }
        }
    );

function drawTotalOrders(groupNumber, events, colorMap) {
    let height = EVENT_HEIGHT + 2 * 15 // padding top bottom = 15
    let width = events.length * EVENT_WIDTH + (events.length - 1) * GAP
    let svg = d3.selectAll(`#rect${groupNumber}`).append("svg").attr("width", width).attr("height", height)

    for (let i = 0; i < events.length;) {
        let polygon
        if (i === 0) {
            // starting events do not have a corner on the left
            polygon = `${i * (EVENT_WIDTH + GAP)},0 ${(i + 1) * (EVENT_WIDTH + GAP)},0 ${(i + 1) * (EVENT_WIDTH + GAP) + EVENT_DIAMETER},${EVENT_DIAMETER} ${(i + 1) * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT} ${i * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT}`
        } else {
            // standard event, not starting and finishing
            polygon = `${i * (EVENT_WIDTH + GAP)},0 ${(i + 1) * (EVENT_WIDTH + GAP)},0 ${(i + 1) * (EVENT_WIDTH + GAP) + EVENT_DIAMETER},${EVENT_DIAMETER} ${(i + 1) * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT} ${i * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT} ${i * (EVENT_WIDTH + GAP) + EVENT_DIAMETER},${EVENT_HEIGHT / 2}`
        }
        svg.append('polygon')
            .attr('points', polygon)
            .attr('fill', colorMap.get(events[i][j][ACTIVITY_KEY]))

        svg.append('text')
            .attr('x', 30 + i * (EVENT_WIDTH + GAP))
            .attr('y', EVENT_HEIGHT + GAP + 30)
            .attr('stroke', 'black')
            .text(events[i][j][ACTIVITY_KEY])
    }
}