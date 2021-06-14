const EVENT_WIDTH = 125
const EVENT_HEIGHT = 50
const GAP = 10
const EVENT_DIAMETER = 25
const ACTIVITY_KEY = 'concept:name'

const combinations = JSON.parse(document.getElementById('combinations').textContent);
axios.get('/partial-order/colors')
    .then((response) => {
            let colorMap = new Map(Object.entries(response.data))
            for (let i = 0; i < combinations.length; i++) {
                drawTotalOrders(i, combinations[i]['events'], colorMap)
            }
        }
    );

function drawTotalOrders(combinationsNumber, events, colorMap) {
    let height = EVENT_HEIGHT
    let width = events.length * EVENT_WIDTH + (events.length - 1) * GAP + EVENT_DIAMETER
    let svg = d3.selectAll(`#combination-${combinationsNumber}`).append("svg").attr("width", width).attr("height", height)

    $(`#combination-${combinationsNumber}`).click(function () {
        redirectPost("/partial-order/delays", {
            "combination": JSON.stringify(events)
        })
    })

    for (let i = 0; i < events.length; i++) {
        let polygon
        if (i === 0) {
            // starting events do not have a corner on the left
            polygon = `${i * (EVENT_WIDTH + GAP)},0 ${(EVENT_WIDTH) + i * (EVENT_WIDTH + GAP)},0 ${EVENT_WIDTH + EVENT_DIAMETER + i * (EVENT_WIDTH + GAP)},${EVENT_DIAMETER} ${EVENT_WIDTH + i * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT} ${i * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT}`
        } else {
            // standard event, not starting and finishing
            polygon = `${i * (EVENT_WIDTH + GAP)},0 ${(EVENT_WIDTH) + i * (EVENT_WIDTH + GAP)},0 ${EVENT_WIDTH + EVENT_DIAMETER + i * (EVENT_WIDTH + GAP)},${EVENT_DIAMETER} ${EVENT_WIDTH + i * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT} ${i * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT} ${EVENT_DIAMETER + i * (EVENT_WIDTH + GAP)},${EVENT_DIAMETER}`
        }
        svg.append('polygon')
            .attr('points', polygon)
            .attr('fill', colorMap.get(events[i][ACTIVITY_KEY]))

        svg.append('text')
            .attr('x', 30 + i * (EVENT_WIDTH + GAP))
            .attr('y', 30)
            .attr('stroke', 'black')
            .text(events[i][ACTIVITY_KEY])
    }
}