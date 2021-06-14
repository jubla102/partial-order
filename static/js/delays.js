let EVENT_WIDTH = 125
let textWidthMap = new Map()
const combination = JSON.parse(document.getElementById('combination').textContent);
axios.get('/partial-order/colors')
    .then((response) => {
            let colorMap = new Map(Object.entries(response.data['colors']))
            let longestActivityWidth = getLongestActivityWidth(response.data['longestActivityName'], '#combination')
            if (longestActivityWidth > EVENT_WIDTH) {
                EVENT_WIDTH = longestActivityWidth
            }
            drawTotalOrder(combination, colorMap)
        }
    );

function drawTotalOrder(events, colorMap) {
    let height = EVENT_HEIGHT
    let width = events.length * EVENT_WIDTH + (events.length - 1) * GAP + EVENT_DIAMETER
    let svg = d3.selectAll(`#combination`).append("svg").attr("width", width).attr("height", height)

    for (let i = 0; i < events.length; i++) {
        let activityName = events[i][ACTIVITY_KEY];
        let polygon
        if (i === 0) {
            // starting events do not have a corner on the left
            polygon = `${i * (EVENT_WIDTH + GAP)},0 ${(EVENT_WIDTH) + i * (EVENT_WIDTH + GAP)},0 ${EVENT_WIDTH + EVENT_DIAMETER + i * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT / 2} ${EVENT_WIDTH + i * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT} ${i * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT}`
        } else {
            // standard event, not starting and finishing
            polygon = `${i * (EVENT_WIDTH + GAP)},0 ${(EVENT_WIDTH) + i * (EVENT_WIDTH + GAP)},0 ${EVENT_WIDTH + EVENT_DIAMETER + i * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT / 2} ${EVENT_WIDTH + i * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT} ${i * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT} ${EVENT_DIAMETER + i * (EVENT_WIDTH + GAP)},${EVENT_HEIGHT / 2}`
        }
        svg.append('polygon')
            .attr('points', polygon)
            .attr('fill', colorMap.get(activityName))

        if (!textWidthMap.has(activityName)) {
            let fasdfasd = svg.append('text')
                .text(activityName)
            textWidthMap.set(activityName, fasdfasd.node().getComputedTextLength())
            fasdfasd.remove()
            console.log(fasdfasd.node().getComputedTextLength())
        }


        if (i === 0) {
            svg.append('text')
                .attr('x', i * (EVENT_WIDTH + GAP) + ((EVENT_WIDTH) / 2) - textWidthMap.get(activityName) / 2)
                .attr('y', 31)
                .text(activityName)
        } else {
            svg.append('text')
                .attr('x', i * (EVENT_WIDTH + GAP) + ((EVENT_WIDTH + EVENT_DIAMETER) / 2) - textWidthMap.get(activityName) / 2)
                .attr('y', 31)
                .text(activityName)
        }

    }
}