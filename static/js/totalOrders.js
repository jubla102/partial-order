let EVENT_WIDTH = 125
const combinations = JSON.parse(document.getElementById('combinations').textContent)
const longestActivityWidth = JSON.parse(document.getElementById('longestActivityWidth').textContent)
const textWidthMap = new Map(JSON.parse(document.getElementById('textWidths').textContent))
axios.get('/partial-order/colors')
    .then((response) => {
            let colorMap = new Map(Object.entries(response.data['colors']))

            if (longestActivityWidth > EVENT_WIDTH) {
                EVENT_WIDTH = longestActivityWidth
            }

            for (let i = 0; i < combinations.length; i++) {
                drawTotalOrders(i, combinations[i]['events'], colorMap)
            }
        }
    );

function drawTotalOrders(combinationsNumber, events, colorMap) {
    let height = EVENT_HEIGHT
    let width = events.length * EVENT_WIDTH + (events.length - 1) * GAP + EVENT_DIAMETER + STROKE_SPACE
    let svg = d3.selectAll(`#combination-${combinationsNumber}`).append("svg").attr("width", width).attr("height", height)

    $(`#combination-${combinationsNumber}`).click(function () {
        redirectPost("/partial-order/delays", {
            "combination": JSON.stringify(events),
            "longestActivityWidth": JSON.stringify(EVENT_WIDTH),
            "textWidths": JSON.stringify([...textWidthMap])
        })
    })

    for (let i = 0; i < events.length; i++) {
        let activityName = events[i][ACTIVITY_KEY]
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
            .attr('class', 'event')
            .attr('fill', colorMap.get(activityName))

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