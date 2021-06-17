const EVENT_WIDTH = 125
const EVENT_HEIGHT = 50
const GAP = 10
const EVENT_DIAMETER = 25
const ACTIVITY_KEY = 'concept:name'
const TIME_KEY = 'time:timestamp'

const combination = JSON.parse(document.getElementById('combination').textContent);

let height = EVENT_HEIGHT * 3
let width = combination.length * EVENT_WIDTH + (combination.length - 1) * GAP + EVENT_DIAMETER
let svg = d3.selectAll(`#combination`).append("svg").attr("width", width).attr("height", height)

axios.get('/partial-order/colors')
    .then((response) => {
            let colorMap = new Map(Object.entries(response.data))
            drawTotalOrder(combination, colorMap)
        }
    );

function drawTotalOrder(events, colorMap) {

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

function visualize_delay() {
    console.log(combination)
    let i = 0, count = 1;
    while (combination[i][TIME_KEY] != combination[i + 1][TIME_KEY])
        i++
    i += 1
    while (i < combination.length - 1) {
        console.log(i, count)
        if (combination[i][TIME_KEY] != combination[i + 1][TIME_KEY]) {
            svg.append('text')
                .attr('x', 30 + i * (EVENT_WIDTH + GAP))
                .attr('y', 70)
                .attr('stroke', 'rgba(92, 184, 92, 1)')
                .text('+' + count + ' delta')

            svg.append('text')
                .attr('x', 32 + i * (EVENT_WIDTH + GAP))
                .attr('y', 90)
                .attr('stroke', 'rgba(92, 184, 92, 1)')
                .text('was added')
                .style("font-size", 14);
            i++
        } else {
            svg.append('text')
                .attr('x', 30 + i * (EVENT_WIDTH + GAP))
                .attr('y', 70)
                .attr('stroke', 'rgba(92, 184, 92, 1)')
                .text('+' + count + ' delta')

            svg.append('text')
                .attr('x', 32 + i * (EVENT_WIDTH + GAP))
                .attr('y', 90)
                .attr('stroke', 'rgba(92, 184, 92, 1)')
                .text('was added')
                .style("font-size", 14);
            count++
            i++
        }
    }
    svg.append('text')
        .attr('x', 30 + i * (EVENT_WIDTH + GAP))
        .attr('y', 70)
        .attr('stroke', 'rgba(92, 184, 92, 1)')
        .text('+' + count + ' delta')

    svg.append('text')
        .attr('x', 32 + i * (EVENT_WIDTH + GAP))
        .attr('y', 90)
        .attr('stroke', 'rgba(92, 184, 92, 1)')
        .text('was added')
        .style("font-size", 14);

}